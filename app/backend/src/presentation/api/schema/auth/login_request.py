"""ログインリクエストスキーマ。"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """ログインリクエスト。

    ログイン時に必要な認証情報。
    """

    email: EmailStr = Field(
        ...,
        description="メールアドレス",
        examples=["user@example.com"],
    )
    password: str = Field(
        ...,
        description="パスワード",
        examples=["SecurePassword123!"],
    )
