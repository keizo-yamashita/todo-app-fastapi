from src.domain.todo.repository import TodoRepository
from src.domain.todo.todo import Todo


class SearchTodosUseCase:

    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    async def execute(self, query: str) -> list[Todo]:
        return await self.todo_repository.search(query)
