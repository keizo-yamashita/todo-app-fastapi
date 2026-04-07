"""Todoテーブルの定義。

SQLAlchemyを使用したデータベースのTodoテーブル構造を定義する。
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.config.database import Base


class TodoModel(Base):
    """Todoテーブル。"""

    __tablename__ = "todos"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    def __repr__(self) -> str:
        """モデルの文字列表現。"""
        return (
            f"<TodoModel(id={self.id}, title={self.title}, completed={self.completed})>"
        )
