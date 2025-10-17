"""ユーザー一覧取得ユースケース。

すべてのユーザーを取得するビジネスロジックを実装する。
"""

from src.domain.user.repository import UserRepository
from src.domain.user.user import User
from src.log.logger import logger
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedTechnicalError,
    ExpectedUseCaseError,
)


class FilterUserUseCase:
    """ユーザー一覧取得ユースケース。

    すべてのユーザーを取得するビジネスロジックを実装する。
    """

    def __init__(self, user_repository: UserRepository) -> None:
        """ユースケースを初期化する。

        Args:
            user_repository: ユーザーリポジトリ

        """
        self.user_repository = user_repository

    async def execute(self) -> list[User]:
        """すべてのユーザーを取得する。

        Returns:
            ユーザーのリスト(ユーザーがいない場合は空リスト)

        Raises:
            ExpectedUseCaseError: ビジネスエラーまたは技術エラーが発生した場合

        """
        try:
            users = await self.user_repository.filter()
        except (ExpectedBusinessError, ExpectedTechnicalError) as e:
            logger.info(
                e.code,
                raw_message=e.raw_message,
                details=e.details,
            )
            raise ExpectedUseCaseError(code=e.code, details=e.details) from e
        return users
