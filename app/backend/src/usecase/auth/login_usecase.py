"""ログインユースケース。

メールアドレスとパスワードで認証し、JWTトークンを発行する。
"""

from dataclasses import dataclass

from src.domain.auth.repository import CredentialRepository
from src.domain.user.email_address import EmailAddress
from src.domain.user.repository import UserRepository
from src.domain.user.user import User
from src.infrastructure.auth.jwt_service import JWTService
from src.infrastructure.auth.password_service import PasswordService
from src.log.logger import logger
from src.shared.errors.codes import AuthErrorCode, CommonErrorCode
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedTechnicalError,
    ExpectedUseCaseError,
)


@dataclass
class LoginRequest:
    """ログインリクエスト。"""

    email: str
    password: str


@dataclass
class LoginResponse:
    """ログインレスポンス。"""

    user: User
    access_token: str


class LoginUseCase:
    """ログインユースケース。

    メールアドレスとパスワードで認証し、JWTトークンを発行する。
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

    async def execute(self, request: LoginRequest) -> LoginResponse:
        """ログインを実行する。

        Args:
            request: ログインリクエスト

        Returns:
            ログインレスポンス

        Raises:
            ExpectedUseCaseError: 認証エラーまたはバリデーションエラー

        """
        def raise_invalid_credentials(email: str) -> None:
            """認証エラーを発生させる。

            Args:
                email: メールアドレス

            Raises:
                ExpectedUseCaseError: 認証エラー

            """
            logger.info(
                "ログインに失敗しました(パスワード不一致)",
                email=email,
            )
            raise ExpectedUseCaseError(
                code=AuthErrorCode.InvalidCredentials,
            )

        try:
            # メールアドレスのバリデーション
            email = EmailAddress(value=request.email)

            # ユーザーを検索
            user = await self._user_repository.find_by_email(email)

            # 認証情報を取得
            credential = await self._credential_repository.find_by_user_id(user.id)

            # パスワードを検証
            if not PasswordService.verify_password(
                request.password, credential.password_hash
            ):
                raise_invalid_credentials(request.email)

            # JWTトークンを生成
            access_token = JWTService.create_access_token(user.id)

            logger.info(
                "ログイン成功",
                user_id=user.id.value,
            )

            return LoginResponse(user=user, access_token=access_token)

        except ValueError as e:
            # ドメインオブジェクトのバリデーションエラー
            logger.info(
                "ログインに失敗しました(バリデーションエラー)",
                error_code=CommonErrorCode.InvalidValue.value,
            )
            raise ExpectedUseCaseError(
                code=CommonErrorCode.InvalidValue,
                details={"error": str(e)},
            ) from e
        except (ExpectedBusinessError, ExpectedTechnicalError) as e:
            # ユーザーが見つからない場合も認証エラーとして扱う
            logger.info(
                "ログインに失敗しました",
                error_code=e.code.value,
            )
            raise ExpectedUseCaseError(
                code=AuthErrorCode.InvalidCredentials,
            ) from e
        except ExpectedUseCaseError:
            # 既にExpectedUseCaseErrorの場合はそのまま再スロー
            raise
