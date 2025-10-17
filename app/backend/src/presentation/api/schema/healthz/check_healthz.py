"""ヘルスチェックレスポンスのスキーマ。

APIのヘルスチェック機能のレスポンス構造を定義する。
"""

from typing import Annotated

from pydantic import BaseModel, Field

from src.presentation.api.schema.safe_str import SafeStr


class CheckHealthResponse(BaseModel):
    """ヘルスチェックレスポンスのスキーマ。

    APIのヘルスチェック機能のレスポンス構造。
    """

    status: Annotated[SafeStr, Field(examples=["OK"], description="APIのステータス")]
