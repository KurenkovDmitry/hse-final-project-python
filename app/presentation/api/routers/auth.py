"""JWT."""

from datetime import UTC, datetime, timedelta
from typing import Annotated, Literal
from uuid import uuid4

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy.exc import IntegrityError

from app.container import get_auth_repository
from app.domain.entities.auth import AuthSession
from app.infrastracture.persistence.auth import AuthRepository

ALGORITHM = "HS256"
ISSUER = "st-api"
AUDIENCE = "st-api"
TOKEN_LIFETIME = timedelta(minutes=15)
MAX_TOKEN_LENGTH = 2048

router = APIRouter()
security = HTTPBearer(auto_error=False)
password_hash = PasswordHash.recommended()
Repository = Annotated[AuthRepository, Depends(get_auth_repository)]
Credentials = Annotated[HTTPAuthorizationCredentials | None, Depends(security)]


class LoginRequest(BaseModel):
    """Вход."""

    model_config = ConfigDict(extra="forbid")

    username: str = Field(
        min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_]+$"
    )
    password: str = Field(min_length=8, max_length=128)


class UserOutput(BaseModel):
    """Данные пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class TokenOutput(BaseModel):
    """Токен."""

    access_token: str
    token_type: Literal["bearer"] = Field(default="bearer")


class TokenClaims(BaseModel):
    """Токен - получение."""

    sub: str = Field(pattern=r"^[1-9][0-9]{0,18}$")
    jti: str = Field(min_length=32, max_length=32, pattern=r"^[0-9a-f]+$")


def unauthorized() -> HTTPException:
    """Единый ответ на неавотризованность."""
    return HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_session(
    request: Request, credentials: Credentials, repository: Repository
) -> AuthSession:
    """Проверка подписи."""
    if credentials is None or len(credentials.credentials) > MAX_TOKEN_LENGTH:
        raise unauthorized()
    try:
        payload = jwt.decode(
            credentials.credentials,
            request.app.state.jwt_secret,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={"require": ["sub", "jti", "iat", "exp"]},
        )
        claims = TokenClaims.model_validate(payload)
    except (jwt.PyJWTError, ValidationError) as err:
        raise unauthorized() from err

    auth_session = repository.get_session(claims.jti)
    if (
        auth_session is None
        or str(auth_session.user_id) != claims.sub
        or auth_session.expires_at <= int(datetime.now(UTC).timestamp())
    ):
        raise unauthorized()
    return auth_session


@router.post("/register", response_model=UserOutput, status_code=201)
def register(credentials: LoginRequest, repository: Repository) -> UserOutput:
    """Регистрация."""
    try:
        user = repository.create_user(
            credentials.username, password_hash.hash(credentials.password)
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=409, detail="Username already registered",
        ) from exc
    return UserOutput.model_validate(user)


@router.post("/login")
def login(
    credentials: LoginRequest,
    request: Request,
    repository: Repository
) -> TokenOutput:
    """Вход."""
    user = repository.get_user(credentials.username)
    if user is None or not password_hash.verify(
        credentials.password, user.password_hash
    ):
        raise unauthorized()

    now = datetime.now(UTC)
    expires_at = now + TOKEN_LIFETIME
    session_id = uuid4().hex
    token = jwt.encode(
        {
            "sub": str(user.id),
            "jti": session_id,
            "iss": ISSUER,
            "aud": AUDIENCE,
            "iat": now,
            "exp": expires_at,
        },
        request.app.state.jwt_secret,
        algorithm=ALGORITHM,
    )
    repository.create_session(
        AuthSession(
            id=session_id,
            user_id=user.id,
            expires_at=int(expires_at.timestamp()),
        ),
        int(now.timestamp()),
    )
    return TokenOutput(access_token=token)


@router.post("/logout", status_code=204)
def logout(
    auth_session: Annotated[AuthSession, Depends(get_current_session)],
    repository: Repository,
) -> Response:
    """Выход."""
    repository.delete_session(auth_session.id)
    return Response(status_code=204)
