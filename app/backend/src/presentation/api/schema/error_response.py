"""エラーレスポンスのスキーマ。

APIエラー時のレスポンス構造を定義する。
"""

from typing import Annotated

from pydantic import BaseModel, Field

from src.presentation.api.schema.safe_str import SafeStr


class ErrorResponse(BaseModel):
    """エラーレスポンスのスキーマ。

    一般的なエラー時のレスポンス構造。
    """

    detail: Annotated[
        SafeStr,
        Field(description="クライアントに表示するエラーメッセージ"),
    ]


class ValidationErrorResponse(BaseModel):
    """バリデーションエラーレスポンスのスキーマ。

    リクエストのバリデーションエラー時のレスポンス構造。
    """

    errors: dict[SafeStr, list[SafeStr]] = Field(
        description="バリデーションエラーの場合のみフィールドごとにエラーの内容を保持する",
        examples=[
            {
                "name": [
                    "string_too_short",
                ],
                "email": ["invalid_email", "missing_keyword_only_argument"],
            },
        ],
    )
