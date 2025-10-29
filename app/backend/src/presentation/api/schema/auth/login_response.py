"""ログインレスポンススキーマ。"""

from pydantic import BaseModel, ConfigDict, Field


class UserInfo(BaseModel):
    """ユーザー情報。"""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="ユーザーID")
    email: str = Field(..., description="メールアドレス")
    name: str = Field(..., description="ユーザー名")
    role: str = Field(..., description="ロール")


class LoginResponse(BaseModel):
    """ログインレスポンス。

    ログインユーザーの情報とアクセストークン。
    """

    user: UserInfo = Field(..., description="ユーザー情報")
    access_token: str = Field(..., description="JWTアクセストークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")
