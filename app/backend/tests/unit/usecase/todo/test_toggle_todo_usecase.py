"""ToggleTodoUseCaseのユニットテスト。"""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.domain.todo.id import TodoId
from src.domain.todo.repository import TodoRepository
from src.domain.todo.todo import Todo
from src.shared.errors.codes import TodoErrorCode
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedUseCaseError,
)
from src.usecase.todo.toggle_todo_usecase import ToggleTodoUseCase


@pytest.fixture
def mock_todo_repository() -> AsyncMock:
    return AsyncMock(spec=TodoRepository)


class TestExecute:
    @pytest.mark.anyio
    async def test_OK_completedがfalseからtrueにトグルされること(
        self,
        mock_todo_repository: AsyncMock,
    ) -> None:
        # arrange
        todo_id = str(uuid4())
        todo = Todo(id=TodoId(value=todo_id), title="テストタスク", completed=False)
        mock_todo_repository.find_by_id.return_value = todo
        mock_todo_repository.save.return_value = todo
        usecase = ToggleTodoUseCase(todo_repository=mock_todo_repository)

        # act
        result = await usecase.execute(TodoId(value=todo_id))

        # assert
        assert result.completed is True
        mock_todo_repository.find_by_id.assert_called_once_with(TodoId(value=todo_id))
        mock_todo_repository.save.assert_called_once()

    @pytest.mark.anyio
    async def test_OK_completedがtrueからfalseにトグルされること(
        self,
        mock_todo_repository: AsyncMock,
    ) -> None:
        # arrange
        todo_id = str(uuid4())
        todo = Todo(id=TodoId(value=todo_id), title="テストタスク", completed=True)
        mock_todo_repository.find_by_id.return_value = todo
        mock_todo_repository.save.return_value = todo
        usecase = ToggleTodoUseCase(todo_repository=mock_todo_repository)

        # act
        result = await usecase.execute(TodoId(value=todo_id))

        # assert
        assert result.completed is False

    @pytest.mark.anyio
    async def test_NG_Todoが存在しない場合はExpectedUseCaseErrorを返すこと(
        self,
        mock_todo_repository: AsyncMock,
    ) -> None:
        # arrange
        todo_id = str(uuid4())
        mock_todo_repository.find_by_id.side_effect = ExpectedBusinessError(
            code=TodoErrorCode.NotFound,
            details={"todo_id": todo_id},
        )
        usecase = ToggleTodoUseCase(todo_repository=mock_todo_repository)

        # act & assert
        with pytest.raises(ExpectedUseCaseError) as exc_info:
            await usecase.execute(TodoId(value=todo_id))

        assert exc_info.value.code == TodoErrorCode.NotFound
        assert exc_info.value.details == {"todo_id": todo_id}
