"""ユーザー関連のAPIエンドポイント。

ユーザーの一覧取得、検索、削除機能を提供する。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db_session, get_user_repository
from src.domain.user.id import UserId
from src.presentation.api.schema.error_response import (
    ErrorResponse,
    ValidationErrorResponse,
)
from src.presentation.api.schema.safe_str import SafeStr
from src.presentation.api.schema.user.create_user_request import CreateUserRequest
from src.presentation.api.schema.user.create_user_response import CreateUserResponse
from src.presentation.api.schema.user.delete_user_response import DeleteUserResponse
from src.presentation.api.schema.user.filter_user_response import FilterUserResponse
from src.presentation.api.schema.user.find_user_response import FindUserResponse
from src.presentation.api.schema.user.user import User as UserSchema
from src.shared.errors.codes import (
    CommonErrorCode,
    UserErrorCode,
)
from src.shared.errors.errors import (
    ExpectedUseCaseError,
)
from src.usecase.user.create_user_usecase import CreateUserUseCase
from src.usecase.user.delete_user_usecase import DeleteUserUseCase
from src.usecase.user.filter_user_usecase import FilterUserUseCase
from src.usecase.user.find_user_usecase import FindUserUseCase

user_router = APIRouter(
    tags=["users"],
)


@user_router.post(
    "/users",
    summary="ユーザーを作成する",
    description="新しいユーザーを作成する",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": CreateUserResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def create_user(
    request: CreateUserRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> CreateUserResponse:
    """新しいユーザーを作成する。

    メールアドレスと名前を指定して新しいユーザーを作成する。
    メールアドレスが既に登録されている場合は400エラーを返す。
    """
    try:
        user_repository = get_user_repository(session)
        user = await CreateUserUseCase(user_repository).execute(request)
        return CreateUserResponse(
            user=UserSchema(
                id=user.id.value,
                email=user.email.value,
                name=user.name.value if user.name else "",
                role=user.role.value.value,
                created_at=user.created_at,
            ),
        )
    except ExpectedUseCaseError as e:
        if e.code == UserErrorCode.EmailAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.code.value,
            ) from e
        raise


@user_router.get(
    "/users",
    summary="ユーザ一覧を取得する",
    description="全てのユーザを取得する",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": FilterUserResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def filter_user(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> FilterUserResponse:
    """すべてのユーザーを取得する。

    システムに登録されているすべてのユーザーの一覧を返す。
    """
    user_repository = get_user_repository(session)
    users = await FilterUserUseCase(user_repository).execute()
    return FilterUserResponse(
        users=[
            UserSchema(
                id=user.id.value,
                email=user.email.value,
                name=user.name.value if user.name else "",
                role=user.role.value.value,
                created_at=user.created_at,
            )
            for user in users
        ],
    )


@user_router.get(
    "/users/{user_id}",
    summary="指定したユーザを取得する",
    description="ユーザIDを指定して単一のユーザを取得する",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": FindUserResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def find_user(
    user_id: Annotated[
        SafeStr,
        Path(description="ユーザID", min_length=1, max_length=128),
    ],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> FindUserResponse:
    """指定したユーザーを取得する。

    ユーザーIDを指定して単一のユーザー情報を取得する。
    ユーザーが存在しない場合は404エラーを返す。
    """
    try:
        user_repository = get_user_repository(session)
        # Presentation層でドメイン型に変換
        domain_user_id = UserId(value=user_id)
        user = await FindUserUseCase(user_repository).execute(domain_user_id)
        return FindUserResponse(
            user=UserSchema(
                id=user.id.value,
                email=user.email.value,
                name=user.name.value if user.name else "",
                role=user.role.value.value,
                created_at=user.created_at,
            ),
        )
    except ExpectedUseCaseError as e:
        if e.code == UserErrorCode.NotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.code.value,
            ) from e
        raise


@user_router.delete(
    "/users/{user_id}",
    summary="ユーザを削除する",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": DeleteUserResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def delete_user(
    user_id: Annotated[
        SafeStr,
        Path(description="ユーザID", min_length=1, max_length=128),
    ],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> DeleteUserResponse:
    """ユーザーを削除する。

    指定したユーザーIDのユーザーをシステムから削除する。
    削除権限がない場合は403エラーを返す。
    """
    try:
        user_repository = get_user_repository(session)
        domain_user_id = UserId(value=user_id)
        await DeleteUserUseCase(user_repository).execute(user_id=domain_user_id)
        return DeleteUserResponse(message="ユーザを削除しました")
    except ExpectedUseCaseError as e:
        if e.code == CommonErrorCode.Forbidden:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=e.code.value,
            ) from e
        if e.code == UserErrorCode.NotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.code.value,
            ) from e
        if e.code == UserErrorCode.UserDeleteError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.code.value,
            ) from e
        raise
