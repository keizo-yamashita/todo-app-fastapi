"""Todo関連のAPIエンドポイント。

Todoの検索と完了フラグ切り替え機能を提供する。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db_session, get_todo_repository
from src.domain.todo.id import TodoId
from src.presentation.api.schema.error_response import (
    ErrorResponse,
    ValidationErrorResponse,
)
from src.presentation.api.schema.safe_str import SafeStr
from src.presentation.api.schema.todo.search_todos_response import SearchTodosResponse
from src.presentation.api.schema.todo.todo import Todo as TodoSchema
from src.presentation.api.schema.todo.toggle_todo_response import ToggleTodoResponse
from src.shared.errors.codes import TodoErrorCode
from src.shared.errors.errors import ExpectedUseCaseError
from src.usecase.todo.search_todos_usecase import SearchTodosUseCase
from src.usecase.todo.toggle_todo_usecase import ToggleTodoUseCase

todo_router = APIRouter(
    tags=["todos"],
)


@todo_router.get(
    "/todos",
    summary="Todoを検索する",
    description="タイトルでTodoを検索する。クエリなしの場合は全件を返す。",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SearchTodosResponse},
    },
)
async def search_todos(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    q: Annotated[str, Query(description="検索クエリ")] = "",
) -> SearchTodosResponse:
    """Todoを検索する。

    タイトルに対して部分一致検索を行う。
    クエリが空の場合は全件を返す。
    """
    todo_repository = get_todo_repository(session)
    usecase = SearchTodosUseCase(todo_repository)
    todos = await usecase.execute(q)
    return SearchTodosResponse(
        todos=[
            TodoSchema(
                id=todo.id.value,
                title=todo.title,
                completed=todo.completed,
                created_at=todo.created_at,
                updated_at=todo.updated_at,
            )
            for todo in todos
        ],
    )


@todo_router.patch(
    "/todos/{todo_id}/toggle",
    summary="Todoの完了フラグを切り替える",
    description="指定IDのTodoのcompletedフラグをトグルする",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ToggleTodoResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def toggle_todo(
    todo_id: Annotated[
        SafeStr,
        Path(description="TodoID", min_length=1, max_length=255),
    ],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ToggleTodoResponse:
    """Todoの完了フラグを切り替える。

    指定したTodoIDのcompletedフラグをトグルする。
    Todoが存在しない場合は404エラーを返す。
    """
    try:
        todo_repository = get_todo_repository(session)
        usecase = ToggleTodoUseCase(todo_repository)
        domain_todo_id = TodoId(value=todo_id)
        todo = await usecase.execute(domain_todo_id)
        return ToggleTodoResponse(
            todo=TodoSchema(
                id=todo.id.value,
                title=todo.title,
                completed=todo.completed,
                created_at=todo.created_at,
                updated_at=todo.updated_at,
            ),
        )
    except ExpectedUseCaseError as e:
        if e.code == TodoErrorCode.NotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.code.value,
            ) from e
        raise
