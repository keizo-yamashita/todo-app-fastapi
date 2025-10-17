"""安全な文字列型の定義。

nullバイトを含まない安全な文字列型を定義する。
"""

from typing import Annotated

from fastapi.exceptions import RequestValidationError
from pydantic import AfterValidator, StrictStr


def validate_no_null_bytes(v: str) -> str:
    """文字列にnullバイトが含まれていないことを検証する。

    Args:
        v: 検証する文字列

    Returns:
        検証済みの文字列

    Raises:
        RequestValidationError: nullバイトが含まれている場合

    """
    if b"\x00" in v.encode():
        raise RequestValidationError(
            [{"type": "value_error", "msg": "String contains null byte"}],
        )
    return v


# StrictStrにnullバイトチェックを追加した型
SafeStr = Annotated[StrictStr, AfterValidator(validate_no_null_bytes)]
