"""新規登録ユースケース。

ユーザーと認証情報を作成する。
"""

from dataclasses import dataclass

from src.domain.auth.credential import Credential
from src.domain.auth.repository import CredentialRepository
from src.domain.user.email_address import EmailAddress
from src.domain.user.name import UserName
from src.domain.user.repository import UserRepository
from src.domain.user.role import Role
from src.domain.user.user import User
from src.infrastructure.auth.password_service import PasswordService
from src.log.logger import logger
from src.shared.errors.codes import CommonErrorCode
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedTechnicalError,
    ExpectedUseCaseError,
)


@dataclass
class RegisterRequest:
    """新規登録リクエスト。"""

    email: str
    name: str
    password: str


@dataclass
class RegisterResponse:
    """新規登録レスポンス。"""

    user: User


class RegisterUseCase:
    """新規登録ユースケース。

    ユーザーと認証情報を作成する。
    """

    def __init__(
        self,
        user_repository: UserRepository,
        credential_repository: CredentialRepository,
    ) -> None:
        """ユースケースを初期化する。

        Args:
            user_repository: ユーザーリポジトリ
            credential_repository: 認証情報リポジトリ

        """
        self._user_repository = user_repository
        self._credential_repository = credential_repository

    async def execute(self, request: RegisterRequest) -> RegisterResponse:
        """新規登録を実行する。

        Args:
            request: 新規登録リクエスト

        Returns:
            新規登録レスポンス

        Raises:
            ExpectedUseCaseError: バリデーションエラーまたはビジネスエラー

        """
        try:
            # デバッグ用: 受け取ったデータのサイズをログ出力
            logger.info(
                "ユーザー登録データ受信",
                email_length=len(request.email),
                name_length=len(request.name),
                password_length=len(request.password),
                password_bytes=len(request.password.encode("utf-8")),
            )

            # ドメインオブジェクトの生成(バリデーション実行)
            email = EmailAddress(value=request.email)
            name = UserName(value=request.name)
            user = User(
                email=email,
                name=name,
                role=Role(),
            )

            # パスワードをハッシュ化
            password_hash = PasswordService.hash_password(request.password)
            credential = Credential(
                user_id=user.id,
                password_hash=password_hash,
            )

            # ユーザーと認証情報を保存
            created_user = await self._user_repository.save(user)
            await self._credential_repository.save(credential)

            logger.info(
                "ユーザー登録完了",
                user_id=created_user.id.value,
            )

        except ValueError as e:
            # ドメインオブジェクトのバリデーションエラー
            logger.info(
                "ユーザー登録に失敗しました(バリデーションエラー)",
                error_code=CommonErrorCode.InvalidValue.value,
                error=str(e),
            )
            raise ExpectedUseCaseError(
                code=CommonErrorCode.InvalidValue,
                details={"error": str(e)},
            ) from e
        except (ExpectedBusinessError, ExpectedTechnicalError) as e:
            logger.info(
                "ユーザー登録に失敗しました",
                error_code=e.code.value,
            )
            raise ExpectedUseCaseError(code=e.code, details=e.details) from e
        else:
            return RegisterResponse(user=created_user)
