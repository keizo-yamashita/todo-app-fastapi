"""Todo完了フラグ切り替えユースケース。

指定IDのTodoのcompletedフラグをトグルする。
"""

from src.domain.todo.id import TodoId
from src.domain.todo.repository import TodoRepository
from src.domain.todo.todo import Todo
from src.log.logger import logger
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedTechnicalError,
    ExpectedUseCaseError,
)


class ToggleTodoUseCase:
    """Todo完了フラグ切り替えユースケース。"""

    def __init__(self, todo_repository: TodoRepository) -> None:
        """ユースケースを初期化する。"""
        self.todo_repository = todo_repository

    async def execute(self, todo_id: TodoId) -> Todo:
        """Todoの完了フラグをトグルする。

        Args:
            todo_id: トグルするTodoのID

        Returns:
            更新されたTodo

        Raises:
            ExpectedUseCaseError: Todoが見つからない場合

        """
        try:
            todo = await self.todo_repository.find_by_id(todo_id)
            todo.toggle()
            return await self.todo_repository.save(todo)
        except (ExpectedBusinessError, ExpectedTechnicalError) as e:
            logger.info(
                e.code,
                raw_message=e.raw_message,
                details=e.details,
            )
            raise ExpectedUseCaseError(code=e.code, details=e.details) from e
