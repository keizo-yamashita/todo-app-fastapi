"""ユーザー作成リクエストスキーマ。

ユーザー作成APIのリクエストボディを定義する。
"""

from typing import Annotated

from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    """ユーザー作成リクエスト。

    新しいユーザーを作成するためのリクエストデータ。
    """

    email: Annotated[
        str,
        Field(
            description="メールアドレス",
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            min_length=1,
            max_length=255,
        ),
    ]
    name: Annotated[
        str,
        Field(
            description="ユーザー名",
            min_length=1,
            max_length=100,
        ),
    ]
