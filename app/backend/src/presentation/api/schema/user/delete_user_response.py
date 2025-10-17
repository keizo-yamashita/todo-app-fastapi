"""ユーザー削除レスポンスのスキーマ。

ユーザー削除APIのレスポンス構造を定義する。
"""

from typing import Annotated

from pydantic import BaseModel, Field

from src.presentation.api.schema.safe_str import SafeStr


class DeleteUserResponse(BaseModel):
    """ユーザー削除レスポンスのスキーマ。

    ユーザー削除APIのレスポンス構造。
    """

    message: Annotated[SafeStr, Field(description="ユーザを削除しました")]
