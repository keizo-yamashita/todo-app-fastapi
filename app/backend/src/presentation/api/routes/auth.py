"""認証APIルーター。

新規登録とログインのAPIエンドポイントを提供する。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db_session
from src.domain.auth.repository import CredentialRepository
from src.domain.user.repository import UserRepository
from src.infrastructure.repository.auth.credential_repository_impl import (
    CredentialRepositoryImpl,
)
from src.infrastructure.repository.user.user_repository_impl import (
    UserRepositoryImpl,
)
from src.presentation.api.schema.auth.login_request import LoginRequest
from src.presentation.api.schema.auth.login_response import (
    LoginResponse,
    UserInfo,
)
from src.presentation.api.schema.auth.register_request import RegisterRequest
from src.presentation.api.schema.auth.register_response import RegisterResponse
from src.shared.errors.codes import (
    AuthErrorCode,
    CommonErrorCode,
    UserErrorCode,
)
from src.shared.errors.errors import ExpectedUseCaseError
from src.usecase.auth.login_usecase import (
    LoginRequest as LoginUseCaseRequest,
)
from src.usecase.auth.login_usecase import (
    LoginUseCase,
)
from src.usecase.auth.register_usecase import (
    RegisterRequest as RegisterUseCaseRequest,
)
from src.usecase.auth.register_usecase import (
    RegisterUseCase,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# OAuth2トークンタイプ
TOKEN_TYPE_BEARER = "bearer"


def get_user_repository(session: AsyncSession) -> UserRepository:
    """ユーザーリポジトリの依存性注入。

    Args:
        session: データベースセッション

    Returns:
        ユーザーリポジトリ

    """
    return UserRepositoryImpl(session)


def get_credential_repository(session: AsyncSession) -> CredentialRepository:
    """認証情報リポジトリの依存性注入。

    Args:
        session: データベースセッション

    Returns:
        認証情報リポジトリ

    """
    return CredentialRepositoryImpl(session)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="新規登録",
    description="新しいユーザーを登録する",
)
async def register(
    request: RegisterRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> RegisterResponse:
    """新規登録エンドポイント。

    Args:
        request: 新規登録リクエスト
        session: データベースセッション

    Returns:
        登録されたユーザー情報

    Raises:
        HTTPException: バリデーションエラーまたはビジネスエラー

    """
    try:
        user_repository = get_user_repository(session)
        credential_repository = get_credential_repository(session)

        usecase = RegisterUseCase(user_repository, credential_repository)
        result = await usecase.execute(
            RegisterUseCaseRequest(
                email=request.email,
                name=request.name,
                password=request.password,
            )
        )

        return RegisterResponse(
            id=result.user.id.value,
            email=result.user.email.value,
            name=result.user.name.value,
            role=result.user.role.value,
        )

    except ExpectedUseCaseError as e:
        if e.code == UserErrorCode.EmailAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.code.value,
            ) from e
        if e.code == CommonErrorCode.InvalidValue:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.code.value,
            ) from e
        raise


@router.post(
    "/login",
    summary="ログイン",
    description="メールアドレスとパスワードでログインする",
)
async def login(
    request: LoginRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> LoginResponse:
    """ログインエンドポイント。

    Args:
        request: ログインリクエスト
        session: データベースセッション

    Returns:
        ユーザー情報とアクセストークン

    Raises:
        HTTPException: 認証エラーまたはバリデーションエラー

    """
    try:
        user_repository = get_user_repository(session)
        credential_repository = get_credential_repository(session)

        usecase = LoginUseCase(user_repository, credential_repository)
        result = await usecase.execute(
            LoginUseCaseRequest(
                email=request.email,
                password=request.password,
            )
        )

        return LoginResponse(
            user=UserInfo(
                id=result.user.id.value,
                email=result.user.email.value,
                name=result.user.name.value,
                role=result.user.role.value,
            ),
            access_token=result.access_token,
            token_type=TOKEN_TYPE_BEARER,
        )

    except ExpectedUseCaseError as e:
        if e.code == AuthErrorCode.InvalidCredentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e.code.value,
            ) from e
        if e.code == CommonErrorCode.InvalidValue:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.code.value,
            ) from e
        raise
