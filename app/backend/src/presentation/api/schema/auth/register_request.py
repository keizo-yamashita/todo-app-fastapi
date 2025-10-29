"""新規登録リクエストスキーマ。"""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """新規登録リクエスト。

    ユーザー登録時に必要な情報。
    """

    email: EmailStr = Field(
        ...,
        description="メールアドレス",
        examples=["user@example.com"],
    )
    name: str = Field(
        ...,
        description="ユーザー名",
        min_length=1,
        max_length=255,
        examples=["John Doe"],
    )
    password: str = Field(
        ...,
        description="パスワード",
        min_length=8,
        max_length=255,
        examples=["SecurePassword123!"],
    )
