"""エラーハンドリングの基底クラス。

アプリケーション全体で使用するエラークラスを定義する。
"""

from typing import Any

from .codes import (
    AuthErrorCode,
    CommonErrorCode,
    TechnicalErrorCode,
    UserErrorCode,
)

type ErrorCode = CommonErrorCode | UserErrorCode | TechnicalErrorCode | AuthErrorCode


class BaseError(Exception):
    """エラーの基底クラス。

    すべてのカスタムエラーの基底となるクラス。
    """

    def __init__(
        self,
        code: ErrorCode,
        raw_message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """エラーを初期化する。

        Args:
            code: エラーコード
            raw_message: 生のエラーメッセージ
            details: エラーの詳細情報

        """
        super().__init__(code)
        self.code: ErrorCode = code
        self.raw_message = raw_message
        self.details = details

    @property
    def message(self) -> str:
        """エラーメッセージを取得する。

        Returns:
            エラーメッセージ

        """
        return str(self.code.value)


class ExpectedBusinessError(BaseError):
    """予期するビジネス例外。

    ビジネスロジック上で想定しうるエラー。
    """


class ExpectedTechnicalError(BaseError):
    """予期する技術的例外。

    システム的・技術的に再現可能なエラー(外部サービス不調など)。
    """


class UnexpectedTechnicalError(BaseError):
    """予期しない技術的例外。

    システム的・技術的に再現可能なエラー(外部サービス不調など)。
    """


class UnexpectedBusinessError(BaseError):
    """予期しないビジネス例外。

    想定外のビジネスロジック上のエラー。
    """


class ExpectedUseCaseError(BaseError):
    """ユースケース上で想定している例外。

    ロジックフロー制御のため意図的に投げるエラーなど。
    """
