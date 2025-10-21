"""CreateUserUseCaseのユニットテスト。

ユーザー作成ユースケースの動作をテストする。
"""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.domain.user.email_address import EmailAddress
from src.domain.user.id import UserId
from src.domain.user.name import UserName
from src.domain.user.repository import UserRepository
from src.domain.user.role import Role, RoleEnum
from src.domain.user.user import User
from src.presentation.api.schema.user.create_user_request import CreateUserRequest
from src.shared.errors.codes import CommonErrorCode, TechnicalErrorCode, UserErrorCode
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedTechnicalError,
    ExpectedUseCaseError,
)
from src.usecase.user.create_user_usecase import CreateUserUseCase


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """モックユーザーリポジトリを作成する。

    Returns:
        モックされたユーザーリポジトリ

    """
    return AsyncMock(spec=UserRepository)


class TestExecute:
    """CreateUserUseCaseの実行テストクラス。

    ユーザー作成ユースケースの実行をテストする。
    """

    @pytest.mark.anyio
    async def test_OK(self, mock_user_repository: AsyncMock) -> None:
        """正常系: ユーザーが正しく作成されることを確認する。"""
        # arrange
        request = CreateUserRequest(
            email="test@example.com",
            name="Test User",
        )
        user_id = str(uuid4())
        expected_user = User(
            id=UserId(value=user_id),
            email=EmailAddress(value=request.email),
            name=UserName(value=request.name),
            role=Role(value=RoleEnum.MEMBER),
        )
        mock_user_repository.save.return_value = expected_user
        create_user_usecase = CreateUserUseCase(user_repository=mock_user_repository)

        # act
        result = await create_user_usecase.execute(request)

        # assert
        assert result.email.value == request.email
        assert result.name.value == request.name
        mock_user_repository.save.assert_called_once()

    @pytest.mark.anyio
    async def test_NG_メールアドレスが既に存在する場合はExpectedUseCaseErrorを返すこと(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        """異常系: メールアドレスが重複している場合にエラーを返す。"""
        # arrange
        request = CreateUserRequest(
            email="duplicate@example.com",
            name="Test User",
        )
        expected_error = ExpectedBusinessError(
            code=UserErrorCode.EmailAlreadyExists,
            details={"email": request.email},
        )
        mock_user_repository.save.side_effect = expected_error
        create_user_usecase = CreateUserUseCase(user_repository=mock_user_repository)

        # act & assert
        with pytest.raises(ExpectedUseCaseError) as exc_info:
            await create_user_usecase.execute(request)

        assert exc_info.value.code == UserErrorCode.EmailAlreadyExists
        assert exc_info.value.details == {"email": request.email}
        mock_user_repository.save.assert_called_once()

    @pytest.mark.anyio
    async def test_NG_ExpectedTechnicalErrorが発生した場合ExpectedUseCaseErrorを返すこと(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        """異常系: 技術的エラーが発生した場合にExpectedUseCaseErrorを返す。"""
        # arrange
        request = CreateUserRequest(
            email="test@example.com",
            name="Test User",
        )
        expected_error = ExpectedTechnicalError(
            code=TechnicalErrorCode.DatabaseConnectionFailed,
            raw_message="Technical error occurred",
            details={"error": "database connection failed"},
        )
        mock_user_repository.save.side_effect = expected_error
        create_user_usecase = CreateUserUseCase(user_repository=mock_user_repository)

        # act & assert
        with pytest.raises(ExpectedUseCaseError) as exc_info:
            await create_user_usecase.execute(request)

        assert exc_info.value.code == TechnicalErrorCode.DatabaseConnectionFailed
        assert exc_info.value.details == {"error": "database connection failed"}
        mock_user_repository.save.assert_called_once()

    @pytest.mark.anyio
    async def test_NG_null文字を含むユーザー名の場合ExpectedUseCaseErrorを返すこと(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        """異常系: null文字を含むユーザー名の場合にExpectedUseCaseErrorを返す。

        Pydanticのバリデーションをパスするが、ドメイン層でエラーになるケース。
        """
        # arrange
        request = CreateUserRequest(
            email="test@example.com",
            name="test\x00user",  # null文字を含む
        )
        create_user_usecase = CreateUserUseCase(user_repository=mock_user_repository)

        # act & assert
        with pytest.raises(ExpectedUseCaseError) as exc_info:
            await create_user_usecase.execute(request)

        assert exc_info.value.code == CommonErrorCode.InvalidValue
        assert "error" in exc_info.value.details
        assert "null character" in exc_info.value.details["error"]
        # バリデーションエラーのためリポジトリは呼ばれない
        mock_user_repository.save.assert_not_called()
