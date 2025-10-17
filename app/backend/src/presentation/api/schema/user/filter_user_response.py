"""ユーザー一覧レスポンスのスキーマ。

ユーザー一覧取得APIのレスポンス構造を定義する。
"""

from pydantic import BaseModel

from src.presentation.api.schema.user.user import User


class FilterUserResponse(BaseModel):
    """ユーザー一覧レスポンスのスキーマ。

    ユーザー一覧取得APIのレスポンス構造。
    """

    users: list[User]
