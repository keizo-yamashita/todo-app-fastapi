"""ユーザー検索ユースケース。

IDでユーザーを検索するビジネスロジックを実装する。
"""

from src.domain.user.id import UserId
from src.domain.user.repository import UserRepository
from src.domain.user.user import User
from src.log.logger import logger
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedTechnicalError,
    ExpectedUseCaseError,
)


class FindUserUseCase:
    """ユーザー検索ユースケース。

    IDでユーザーを検索するビジネスロジックを実装する。
    """

    def __init__(self, user_repository: UserRepository) -> None:
        """ユースケースを初期化する。

        Args:
            user_repository: ユーザーリポジトリ

        """
        self.user_repository = user_repository

    async def execute(self, user_id: UserId) -> User:
        """ユーザーを検索する。

        Args:
            user_id: 検索するユーザーID

        Returns:
            見つかったユーザー

        Raises:
            ExpectedUseCaseError: ビジネスエラーまたは技術エラーが発生した場合

        """
        try:
            return await self.user_repository.find_by_id(user_id)
        except (ExpectedBusinessError, ExpectedTechnicalError) as e:
            logger.info(
                e.code,
                raw_message=e.raw_message,
                details=e.details,
            )
            raise ExpectedUseCaseError(code=e.code, details=e.details) from e
