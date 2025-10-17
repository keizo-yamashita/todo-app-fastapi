"""DeleteUserUseCaseのユニットテスト。

ユーザー削除ユースケースの動作をテストする。
"""

from unittest.mock import AsyncMock

import pytest

from src.domain.user.repository import UserRepository
from src.domain.user.role import Role, RoleEnum
from src.domain.user.user import User
from src.shared.errors.codes import UserErrorCode
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedUseCaseError,
)
from src.usecase.user.delete_user_usecase import DeleteUserUseCase


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    return AsyncMock(spec=UserRepository)


class TestExecute:
    """DeleteUserUseCaseの実行テストクラス。

    ユーザー削除ユースケースの実行をテストする。
    """

    @pytest.mark.anyio
    async def test_OK(self, mock_user_repository: AsyncMock) -> None:
        # arrange
        user = User.random()
        mock_user_repository.delete.return_value = user.id
        deleteuserusecase = DeleteUserUseCase(
            user_repository=mock_user_repository,
        )

        # act
        await deleteuserusecase.execute(user_id=user.id)

        # assert
        assert True

    @pytest.mark.anyio
    async def test_NG_存在しないユーザIDを指定した場合ExpectedUseCaseErrorが返ること(
        self,
        mock_user_repository: AsyncMock,
    ) -> None:
        # arrange
        user = User.random()
        mock_user_repository.delete.return_value = user.id
        mock_user_repository.delete.side_effect = ExpectedBusinessError(
            code=UserErrorCode.NotFound,
            raw_message="テスト",
            details={"user_id": user.id},
        )
        deleteuserusecase = DeleteUserUseCase(
            user_repository=mock_user_repository,
        )

        # act & assert
        with pytest.raises(ExpectedUseCaseError) as e:
            await deleteuserusecase.execute(user_id=user.id)
        assert e.value.code == UserErrorCode.NotFound

    @pytest.mark.anyio
    async def test_OK_is_allowedメソッドでSUPERADMINとADMINは削除可能であること(
        self,
    ) -> None:
        # arrange
        superadmin_user = User.random(role=Role(value=RoleEnum.SUPERADMIN))
        admin_user = User.random(role=Role(value=RoleEnum.ADMIN))

        # act & assert
        assert DeleteUserUseCase.is_allowed(superadmin_user) is True
        assert DeleteUserUseCase.is_allowed(admin_user) is True

    @pytest.mark.anyio
    async def test_NG_is_allowedメソッドでMEMBERは削除不可であること(self) -> None:
        # arrange
        member_user = User.random(role=Role(value=RoleEnum.MEMBER))

        # act & assert
        assert DeleteUserUseCase.is_allowed(member_user) is False
