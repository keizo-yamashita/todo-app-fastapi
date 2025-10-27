"""ユーザー作成レスポンススキーマ。

ユーザー作成APIのレスポンスボディを定義する。
"""

from typing import Annotated

from pydantic import BaseModel, Field

from src.presentation.api.schema.user.user import User


class CreateUserResponse(BaseModel):
    """ユーザー作成レスポンス。

    作成されたユーザーの情報を返す。
    """

    user: Annotated[
        User,
        Field(description="作成されたユーザー"),
    ]
