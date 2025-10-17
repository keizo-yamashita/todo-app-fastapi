"""FilterUserUseCaseのユニットテスト。

ユーザー一覧取得ユースケースの動作をテストする。
"""

from unittest.mock import AsyncMock

import pytest

from src.domain.user.email_address import EmailAddress
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
from src.usecase.user.filter_user_usecase import FilterUserUseCase


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    return AsyncMock(spec=UserRepository)


class TestExecute:
    """FilterUserUseCaseの実行テストクラス。

    ユーザー一覧取得ユースケースの実行をテストする。
    """

    @pytest.mark.anyio
    async def test_OK(self, mock_user_repository: AsyncMock) -> None:
        # arrange
        test_users = [
            User(
                email=EmailAddress.random(),
                role=Role(value=RoleEnum.MEMBER),
                name=UserName.random(),
            )
            for _ in range(3)
        ]
        mock_user_repository.filter.return_value = test_users
        filter_user_usecase = FilterUserUseCase(user_repository=mock_user_repository)

        # act
        result = await filter_user_usecase.execute()

        # assert
        assert result == test_users
        mock_user_repository.filter.assert_called_once()
        for res in result:
            assert isinstance(res, User)

    @pytest.mark.anyio
    async def test_NG_ユーザが取得できなかった場合は空配列を返すこと(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        # arrange
        mock_user_repository.filter.return_value = []
        filter_user_usecase = FilterUserUseCase(user_repository=mock_user_repository)

        # act
        result = await filter_user_usecase.execute()

        # assert
        assert result == []
        mock_user_repository.filter.assert_called_once()

    @pytest.mark.anyio
    async def test_NG_ExpectedBusinessErrorが発生した場合ExpectedUseCaseErrorを返すこと(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        # arrange
        expected_error = ExpectedBusinessError(
            code=UserErrorCode.NotFound,
            raw_message="Business error occurred",
            details={"key": "value"},
        )
        mock_user_repository.filter.side_effect = expected_error
        filter_user_usecase = FilterUserUseCase(user_repository=mock_user_repository)

        # act & assert
        with pytest.raises(ExpectedUseCaseError) as exc_info:
            await filter_user_usecase.execute()

        assert exc_info.value.code == UserErrorCode.NotFound
        assert exc_info.value.details == {"key": "value"}
        mock_user_repository.filter.assert_called_once()

    @pytest.mark.anyio
    async def test_NG_ExpectedTechnicalErrorが発生した場合ExpectedUseCaseErrorを返すこと(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        # arrange
        expected_error = ExpectedTechnicalError(
            code=TechnicalErrorCode.DatabaseConnectionFailed,
            raw_message="Technical error occurred",
            details={"error": "connection failed"},
        )
        mock_user_repository.filter.side_effect = expected_error
        filter_user_usecase = FilterUserUseCase(user_repository=mock_user_repository)

        # act & assert
        with pytest.raises(ExpectedUseCaseError) as exc_info:
            await filter_user_usecase.execute()

        assert exc_info.value.code == TechnicalErrorCode.DatabaseConnectionFailed
        assert exc_info.value.details == {"error": "connection failed"}
        mock_user_repository.filter.assert_called_once()
