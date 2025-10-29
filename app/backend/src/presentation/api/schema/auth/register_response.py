"""新規登録レスポンススキーマ。"""

from pydantic import BaseModel, ConfigDict, Field


class RegisterResponse(BaseModel):
    """新規登録レスポンス。

    登録されたユーザー情報。
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="ユーザーID")
    email: str = Field(..., description="メールアドレス")
    name: str = Field(..., description="ユーザー名")
    role: str = Field(..., description="ロール")
