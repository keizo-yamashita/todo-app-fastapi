"""Todoトグルレスポンスのスキーマ。"""

from pydantic import BaseModel

from src.presentation.api.schema.todo.todo import Todo


class ToggleTodoResponse(BaseModel):
    """Todoトグルレスポンスのスキーマ。"""

    todo: Todo
