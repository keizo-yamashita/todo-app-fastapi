"""ユーザー検索レスポンスのスキーマ。

ユーザー検索APIのレスポンス構造を定義する。
"""

from pydantic import BaseModel

from src.presentation.api.schema.user.user import User


class FindUserResponse(BaseModel):
    """ユーザー検索レスポンスのスキーマ。

    ユーザー検索APIのレスポンス構造。
    """

    user: User
