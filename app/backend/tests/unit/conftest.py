"""ユニットテスト用の共通設定。

ユニットテストで使用する共通のフィクスチャを定義する。
"""

import pytest


@pytest.fixture(scope="session", autouse=False)
def disable_db_connection() -> None:
    """データベース接続を無効化するフィクスチャ。

    ユニットテストでデータベース接続が不要な場合に使用する。
    """
