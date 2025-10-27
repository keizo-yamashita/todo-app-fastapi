"""FindUserUseCaseのユニットテスト。

ユーザー検索ユースケースの動作をテストする。
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
from src.shared.errors.codes import TechnicalErrorCode, UserErrorCode
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedTechnicalError,
    ExpectedUseCaseError,
)
from src.usecase.user.find_user_usecase import FindUserUseCase


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    return AsyncMock(spec=UserRepository)


class TestExecute:
    """FindUserUseCaseの実行テストクラス。

    ユーザー検索ユースケースの実行をテストする。
    """

    @pytest.mark.anyio
    async def test_OK(self, mock_user_repository: AsyncMock) -> None:
        # arrange
        user_id = str(uuid4())
        test_user = User(
            id=UserId(value=user_id),
            email=EmailAddress(value="fumiaki.kobayashi@galirage.com"),
            role=Role(value=RoleEnum.MEMBER),
            name=UserName(value="test_name"),
        )
        mock_user_repository.find_by_id.return_value = test_user
        find_user_usecase = FindUserUseCase(user_repository=mock_user_repository)
        domain_user_id = UserId(value=user_id)

        # act
        result = await find_user_usecase.execute(domain_user_id)

        # assert
        assert result == test_user
        mock_user_repository.find_by_id.assert_called_once_with(UserId(value=user_id))

    @pytest.mark.anyio
    async def test_NG_ユーザーが存在しない場合はExpectedUseCaseErrorを返すこと(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        # arrange
        domain_user_id = UserId()
        mock_user_repository.find_by_id.side_effect = ExpectedUseCaseError(
            code=UserErrorCode.NotFound,
            details={"user_id": domain_user_id.value},
        )
        find_user_usecase = FindUserUseCase(user_repository=mock_user_repository)

        # act & assert
        with pytest.raises(ExpectedUseCaseError):
            await find_user_usecase.execute(domain_user_id)

    @pytest.mark.anyio
    async def test_NG_ExpectedBusinessErrorが発生した場合ExpectedUseCaseErrorを返すこと(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        # arrange
        user_id = str(uuid4())
        domain_user_id = UserId(value=user_id)
        expected_error = ExpectedBusinessError(
            code=UserErrorCode.NotFound,
            raw_message="User not found",
            details={"user_id": user_id},
        )
        mock_user_repository.find_by_id.side_effect = expected_error
        find_user_usecase = FindUserUseCase(user_repository=mock_user_repository)

        # act & assert
        with pytest.raises(ExpectedUseCaseError) as exc_info:
            await find_user_usecase.execute(domain_user_id)

        assert exc_info.value.code == UserErrorCode.NotFound
        assert exc_info.value.details == {"user_id": user_id}
        mock_user_repository.find_by_id.assert_called_once_with(UserId(value=user_id))

    @pytest.mark.anyio
    async def test_NG_ExpectedTechnicalErrorが発生した場合ExpectedUseCaseErrorを返すこと(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        # arrange
        user_id = str(uuid4())
        domain_user_id = UserId(value=user_id)
        expected_error = ExpectedTechnicalError(
            code=TechnicalErrorCode.DatabaseConnectionFailed,
            raw_message="Technical error occurred",
            details={"error": "database connection failed"},
        )
        mock_user_repository.find_by_id.side_effect = expected_error
        find_user_usecase = FindUserUseCase(user_repository=mock_user_repository)

        # act & assert
        with pytest.raises(ExpectedUseCaseError) as exc_info:
            await find_user_usecase.execute(domain_user_id)

        assert exc_info.value.code == TechnicalErrorCode.DatabaseConnectionFailed
        assert exc_info.value.details == {"error": "database connection failed"}
        mock_user_repository.find_by_id.assert_called_once_with(UserId(value=user_id))
