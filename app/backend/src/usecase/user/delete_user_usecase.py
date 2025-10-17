"""ユーザー削除ユースケース。

ユーザーを削除するビジネスロジックを実装する。
"""

from src.domain.user.id import UserId
from src.domain.user.repository import UserRepository
from src.domain.user.role import RoleEnum
from src.domain.user.user import User
from src.log.logger import logger
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedTechnicalError,
    ExpectedUseCaseError,
)


class DeleteUserUseCase:
    """ユーザー削除ユースケース。

    ユーザーを削除するビジネスロジックを実装する。
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        """ユースケースを初期化する。

        Args:
            user_repository: ユーザーリポジトリ

        """
        self.user_repository = user_repository

    async def execute(
        self,
        user_id: UserId,
    ) -> None:
        """ユーザーを削除する。

        Args:
            user_id: 削除するユーザーID

        Raises:
            ExpectedUseCaseError: ビジネスエラーまたは技術エラーが発生した場合

        """
        try:
            user = await self.user_repository.find_by_id(user_id)
            await self.user_repository.delete(user_id=user.id)
        except (ExpectedBusinessError, ExpectedTechnicalError) as e:
            logger.info(
                e.code,
                raw_message=e.raw_message,
                details=e.details,
            )
            raise ExpectedUseCaseError(code=e.code, details=e.details) from e

    @staticmethod
    def is_allowed(current_user: User) -> bool:
        """ユーザー削除が許可されているかチェックする。

        Args:
            current_user: 現在のユーザー

        Returns:
            削除が許可されている場合はTrue

        """
        return current_user.role.value in {
            RoleEnum.SUPERADMIN,
            RoleEnum.ADMIN,
        }
