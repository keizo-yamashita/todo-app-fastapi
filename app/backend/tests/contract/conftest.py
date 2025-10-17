"""契約テスト専用の設定。

契約テストはAPIサーバーが起動している前提で動作するため、
データベース接続やマイグレーションは不要。
"""

import pytest


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """APIサーバーのベースURL"""
    import os

    return os.getenv("API_BASE_URL", "http://localhost:8000")
