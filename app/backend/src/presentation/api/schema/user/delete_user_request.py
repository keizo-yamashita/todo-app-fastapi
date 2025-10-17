"""ユーザー削除リクエストのスキーマ。

ユーザー削除APIで使用するリクエストパラメータを定義する。
"""

from typing import Annotated

from pydantic import BaseModel, Field

from src.presentation.api.schema.safe_str import SafeStr


class DeleteUserRequest(BaseModel):
    """ユーザー削除リクエストのスキーマ。

    ユーザー削除APIで使用するリクエストパラメータ。
    """

    user_id: Annotated[
        SafeStr,
        Field(description="ユーザID", min_length=1, max_length=128),
    ]
