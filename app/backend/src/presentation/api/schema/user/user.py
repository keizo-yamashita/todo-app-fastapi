"""ユーザー情報のAPIスキーマ。

APIレスポンスで使用するユーザー情報の構造を定義する。
"""

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from src.presentation.api.schema.safe_str import SafeStr


class User(BaseModel):
    """ユーザー情報のAPIスキーマ。

    APIレスポンスで使用するユーザー情報の構造。
    """

    id: Annotated[SafeStr, Field(description="ユーザーID")]
    email: Annotated[SafeStr, Field(description="メールアドレス")]
    role: Annotated[
        Literal["superadmin", "admin", "member"],
        Field(description="ロール"),
    ]
    name: Annotated[SafeStr, Field(description="ユーザー名")]
    created_at: datetime = Field(description="作成日時")
