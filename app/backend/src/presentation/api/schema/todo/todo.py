"""Todoスキーマ。

APIレスポンスで使用するTodoの構造を定義する。
"""

from datetime import datetime

from pydantic import BaseModel, Field


class Todo(BaseModel):
    """Todoのレスポンススキーマ。"""

    id: str = Field(description="TodoID")
    title: str = Field(description="タイトル")
    completed: bool = Field(description="完了フラグ")
    created_at: datetime = Field(description="作成日時")
    updated_at: datetime = Field(description="更新日時")
