"""Todoエンティティのユニットテスト。"""

from datetime import datetime

from src.domain.todo.id import TodoId
from src.domain.todo.todo import Todo


class TestInit:
    def test_OK_生成できること(self) -> None:
        todo = Todo(title="テストタスク")

        assert isinstance(todo, Todo)
        assert todo.title == "テストタスク"
        assert todo.completed is False
        assert isinstance(todo.id, TodoId)
        assert isinstance(todo.created_at, datetime)
        assert isinstance(todo.updated_at, datetime)


class TestToggle:
    def test_OK_falseからtrueに切り替わること(self) -> None:
        todo = Todo(title="テストタスク", completed=False)
        original_updated_at = todo.updated_at

        todo.toggle()

        assert todo.completed is True
        assert todo.updated_at >= original_updated_at

    def test_OK_trueからfalseに切り替わること(self) -> None:
        todo = Todo(title="テストタスク", completed=True)

        todo.toggle()

        assert todo.completed is False

    def test_OK_2回トグルすると元に戻ること(self) -> None:
        todo = Todo(title="テストタスク", completed=False)

        todo.toggle()
        todo.toggle()

        assert todo.completed is False


class TestEquality:
    def test_OK_同じIDのTodoは等しいこと(self) -> None:
        todo_id = TodoId(value="same-id")
        todo1 = Todo(id=todo_id, title="タスク1")
        todo2 = Todo(id=todo_id, title="タスク2")

        assert todo1 == todo2

    def test_OK_異なるIDのTodoは等しくないこと(self) -> None:
        todo1 = Todo(id=TodoId(value="id-1"), title="タスク1")
        todo2 = Todo(id=TodoId(value="id-2"), title="タスク2")

        assert todo1 != todo2
