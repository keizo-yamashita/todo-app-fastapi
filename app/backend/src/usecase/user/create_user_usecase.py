"""ユーザー作成ユースケース。

新しいユーザーを作成するビジネスロジックを実装する。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.domain.user.email_address import EmailAddress
from src.domain.user.name import UserName
from src.domain.user.user import User
from src.log.logger import logger
from src.shared.errors.codes import CommonErrorCode
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedTechnicalError,
    ExpectedUseCaseError,
)

if TYPE_CHECKING:
    from src.domain.user.repository import UserRepository
    from src.presentation.api.schema.user.create_user_request import (
        CreateUserRequest,
    )


class CreateUserUseCase:
    """ユーザー作成ユースケース。

    新しいユーザーを作成し、データベースに保存する。
    メールアドレスの重複チェックを行う。
    """

    def __init__(self, user_repository: UserRepository) -> None:
        """ユースケースを初期化する。

        Args:
            user_repository: ユーザーリポジトリ

        """
        self._user_repository = user_repository

    async def execute(self, request: CreateUserRequest) -> User:
        """ユーザーを作成する。

        Args:
            request: ユーザー作成リクエスト

        Returns:
            作成されたユーザー

        Raises:
            ExpectedUseCaseError: ユーザー作成に失敗した場合

        """
        try:
            email = EmailAddress(value=request.email)
            name = UserName(value=request.name)
            user = User(email=email, name=name)

            created_user = await self._user_repository.save(user)

            logger.info(
                "ユーザー作成完了",
                user_id=created_user.id.value,
                email=created_user.email.value,
            )

        except ValueError as e:
            # ドメインオブジェクトのバリデーションエラー
            logger.info(
                "ユーザー作成に失敗しました（バリデーションエラー）",
                error=str(e),
            )
            raise ExpectedUseCaseError(
                code=CommonErrorCode.InvalidValue,
                details={"error": str(e)},
            ) from e
        except (ExpectedBusinessError, ExpectedTechnicalError) as e:
            logger.info(
                "ユーザー作成に失敗しました",
                raw_message=e.raw_message,
                details=e.details,
            )
            raise ExpectedUseCaseError(code=e.code, details=e.details) from e
        else:
            return created_user
