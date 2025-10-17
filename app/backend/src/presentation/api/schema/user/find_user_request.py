"""ユーザー検索リクエストのスキーマ。

ユーザー検索APIで使用するリクエストパラメータを定義する。
"""

from typing import Annotated

from pydantic import BaseModel, Field

from src.presentation.api.schema.safe_str import SafeStr


class FindUserRequest(BaseModel):
    """ユーザー検索リクエストのスキーマ。

    ユーザー検索APIで使用するリクエストパラメータ。
    """

    user_id: Annotated[
        SafeStr,
        Field(description="ユーザーID", min_length=1, max_length=128),
    ]
