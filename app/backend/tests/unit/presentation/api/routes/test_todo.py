"""GET /todos?q= と PATCH /todos/:id/toggle のテスト。

TestClientを使用し、正常系・異常系をカバーする。
インメモリのフェイクリポジトリでDB依存なしで実行可能。
"""

import uuid
from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.domain.todo.id import TodoId
from src.domain.todo.repository import TodoRepository
from src.domain.todo.todo import Todo
from src.main import app
from src.shared.errors.codes import TodoErrorCode
from src.shared.errors.errors import ExpectedBusinessError


class FakeTodoRepository(TodoRepository):
    """テスト用のインメモリTodoリポジトリ。"""

    def __init__(self) -> None:
        self._store: dict[str, Todo] = {}

    def add(self, todo: Todo) -> None:
        self._store[todo.id.value] = todo

    async def search(self, query: str) -> list[Todo]:
        if not query:
            return list(self._store.values())
        q = query.lower()
        return [t for t in self._store.values() if q in t.title.lower()]

    async def find_by_id(self, todo_id: TodoId) -> Todo:
        todo = self._store.get(todo_id.value)
        if todo is None:
            raise ExpectedBusinessError(
                code=TodoErrorCode.NotFound,
                details={"todo_id": todo_id.value},
            )
        return todo

    async def save(self, todo: Todo) -> Todo:
        self._store[todo.id.value] = todo
        return todo


_fake_repo = FakeTodoRepository()


def _fake_get_todo_repository(_session):
    return _fake_repo


def _make_todo(title: str, completed: bool = False) -> Todo:
    """テスト用Todoを作成してリポジトリに追加し、返す。"""
    now = datetime.now(UTC)
    todo = Todo(
        id=TodoId(value=str(uuid.uuid4())),
        title=title,
        completed=completed,
        created_at=now,
        updated_at=now,
    )
    _fake_repo.add(todo)
    return todo


@pytest.fixture(autouse=True)
def _setup():
    """各テスト前にリポジトリをクリアし、依存性をパッチする。"""
    _fake_repo._store.clear()
    with patch(
        "src.presentation.api.routes.todo.get_todo_repository",
        _fake_get_todo_repository,
    ):
        yield


client = TestClient(app, root_path="/api")


# ======================================================================
# GET /todos?q= (検索エンドポイント)
# ======================================================================


class TestSearchTodos:
    """GET /todos のテスト。"""

    def test_empty_db_returns_empty_list(self):
        """DBが空のとき、空リストを返す。"""
        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert data["todos"] == []

    def test_returns_all_todos_without_query(self):
        """クエリなしで全件を返す。"""
        _make_todo("買い物")
        _make_todo("掃除")

        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 2

    def test_search_filters_by_title(self):
        """qパラメータでタイトル部分一致フィルタリングする。"""
        _make_todo("買い物に行く")
        _make_todo("掃除する")
        _make_todo("買い物リスト作成")

        response = client.get("/todos", params={"q": "買い物"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 2
        titles = {t["title"] for t in data["todos"]}
        assert "買い物に行く" in titles
        assert "買い物リスト作成" in titles

    def test_search_no_match_returns_empty(self):
        """一致しないクエリで空リストを返す。"""
        _make_todo("買い物")

        response = client.get("/todos", params={"q": "ランニング"})
        assert response.status_code == 200
        data = response.json()
        assert data["todos"] == []

    def test_search_is_case_insensitive(self):
        """検索は大文字小文字を区別しない。"""
        _make_todo("Buy Groceries")
        _make_todo("Clean house")

        response = client.get("/todos", params={"q": "buy"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 1
        assert data["todos"][0]["title"] == "Buy Groceries"

    def test_search_returns_completed_status(self):
        """完了状態のTodoも含めて返す。"""
        _make_todo("完了済みタスク", completed=True)
        _make_todo("未完了タスク", completed=False)

        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 2
        completed = [t for t in data["todos"] if t["completed"]]
        assert len(completed) == 1

    def test_todo_response_schema(self):
        """レスポンスのスキーマが正しい。"""
        _make_todo("スキーマ確認")

        response = client.get("/todos")
        assert response.status_code == 200
        todo = response.json()["todos"][0]
        assert "id" in todo
        assert "title" in todo
        assert "completed" in todo
        assert "created_at" in todo
        assert "updated_at" in todo


# ======================================================================
# PATCH /todos/:id/toggle (トグルエンドポイント)
# ======================================================================


class TestToggleTodo:
    """PATCH /todos/:id/toggle のテスト。"""

    def test_toggle_uncompleted_to_completed(self):
        """未完了→完了にトグルする。"""
        todo = _make_todo("トグルテスト", completed=False)

        response = client.patch(f"/todos/{todo.id.value}/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["todo"]["id"] == todo.id.value
        assert data["todo"]["completed"] is True

    def test_toggle_completed_to_uncompleted(self):
        """完了→未完了にトグルする。"""
        todo = _make_todo("トグルテスト2", completed=True)

        response = client.patch(f"/todos/{todo.id.value}/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["todo"]["completed"] is False

    def test_double_toggle_restores_state(self):
        """2回トグルすると元の状態に戻る。"""
        todo = _make_todo("ダブルトグル", completed=False)

        client.patch(f"/todos/{todo.id.value}/toggle")
        response = client.patch(f"/todos/{todo.id.value}/toggle")
        assert response.status_code == 200
        assert response.json()["todo"]["completed"] is False

    def test_toggle_nonexistent_returns_404(self):
        """存在しないTodoのトグルで404を返す。"""
        fake_id = str(uuid.uuid4())
        response = client.patch(f"/todos/{fake_id}/toggle")
        assert response.status_code == 404

    def test_toggle_404_response_body(self):
        """404レスポンスのボディにエラー詳細が含まれる。"""
        fake_id = str(uuid.uuid4())
        response = client.patch(f"/todos/{fake_id}/toggle")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "TODO_NOT_FOUND"

    def test_toggle_preserves_title(self):
        """トグル後もタイトルが維持される。"""
        todo = _make_todo("タイトル保持テスト")

        response = client.patch(f"/todos/{todo.id.value}/toggle")
        assert response.status_code == 200
        assert response.json()["todo"]["title"] == "タイトル保持テスト"

    def test_toggle_response_schema(self):
        """トグルレスポンスのスキーマが正しい。"""
        todo = _make_todo("スキーマ確認")

        response = client.patch(f"/todos/{todo.id.value}/toggle")
        assert response.status_code == 200
        resp_todo = response.json()["todo"]
        assert "id" in resp_todo
        assert "title" in resp_todo
        assert "completed" in resp_todo
        assert "created_at" in resp_todo
        assert "updated_at" in resp_todo
