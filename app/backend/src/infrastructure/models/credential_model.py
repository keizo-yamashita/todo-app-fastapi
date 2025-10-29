"""認証情報テーブルの定義。

SQLAlchemyを使用したデータベースの認証情報テーブル構造を定義する。
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.config.database import Base


class CredentialModel(Base):
    """認証情報テーブル。

    ユーザーの認証情報(パスワードハッシュ)を格納するデータベーステーブル。
    SQLAlchemy 2.0のMapped型を使用した型安全なモデル定義。
    """

    __tablename__ = "credentials"

    # 主キー兼外部キー(ユーザーID)
    user_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # パスワードハッシュ(bcrypt)
    password_hash: Mapped[str] = mapped_column(String(255))

    # 作成日時(デフォルト: 現在時刻)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    # 更新日時(デフォルト: 現在時刻)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self) -> str:
        """モデルの文字列表現。

        Returns:
            モデルの文字列表現

        """
        return f"<CredentialModel(user_id={self.user_id})>"
