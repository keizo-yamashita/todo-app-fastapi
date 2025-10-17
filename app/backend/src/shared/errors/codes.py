"""エラーコードの定義。

アプリケーション全体で使用するエラーコードを定義する。
"""

from enum import Enum


class CommonErrorCode(str, Enum):
    """共通エラーコード。

    アプリケーション全体で共通して使用されるエラーコード。
    """

    Unauthorized = "UNAUTHORIZED"
    Forbidden = "FORBIDDEN"
    InvalidValue = "INVALID_VALUE"
    UnexpectedError = "UNEXPECTED_ERROR"
    ConfigurationError = "CONFIGURATION_ERROR"


class TechnicalErrorCode(str, Enum):
    """技術的エラーコード。

    システム的・技術的なエラーコード。
    """

    DatabaseOperationFailed = "DATABASE_OPERATION_FAILED"
    DatabaseQueryFailed = "DATABASE_QUERY_FAILED"
    DatabaseConnectionFailed = "DATABASE_CONNECTION_FAILED"


class UserErrorCode(str, Enum):
    """ユーザー関連のエラーコード。

    ユーザー操作に関するエラーコード。
    """

    NotFound = "USER_NOT_FOUND"
    EmailAlreadyExists = "USER_EMAIL_ALREADY_EXISTS"
    UserDeleteError = "USER_DELETE_ERROR"
