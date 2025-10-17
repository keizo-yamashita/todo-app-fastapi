"""ユーザーテーブルの定義。

SQLAlchemyを使用したデータベースのユーザーテーブル構造を定義する。
"""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.config.database import Base


class UserModel(Base):
    """ユーザーテーブル。

    ユーザー情報を格納するデータベーステーブル。
    SQLAlchemy 2.0のMapped型を使用した型安全なモデル定義。
    """

    __tablename__ = "users"

    # 主キー(UUID文字列)
    id: Mapped[str] = mapped_column(String(255), primary_key=True)

    # メールアドレス(一意制約、インデックス付き)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    # ユーザー名
    name: Mapped[str] = mapped_column(String(255))

    # ロール(user, admin等)
    role: Mapped[str] = mapped_column(String(50))

    # 作成日時(デフォルト: 現在時刻)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    def __repr__(self) -> str:
        """モデルの文字列表現。

        Returns:
            モデルの文字列表現

        """
        return f"<UserModel(id={self.id}, email={self.email}, name={self.name})>"
