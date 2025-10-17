"""環境設定の管理。

アプリケーションの実行環境を管理する。
"""

import os
from enum import Enum


class Environment(str, Enum):
    """実行環境の定義。

    アプリケーションの実行環境を表す列挙型。
    """

    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"

    @staticmethod
    def is_production() -> bool:
        """本番環境かどうかを判定する。

        Returns:
            本番環境の場合はTrue

        """
        return (
            Environment(os.environ.get("ENVIRONMENT", Environment.LOCAL))
            == Environment.PRODUCTION
        )

    @staticmethod
    def is_staging() -> bool:
        """ステージング環境かどうかを判定する。

        Returns:
            ステージング環境の場合はTrue

        """
        return (
            Environment(os.environ.get("ENVIRONMENT", Environment.LOCAL))
            == Environment.STAGING
        )

    @staticmethod
    def is_local() -> bool:
        """ローカル環境かどうかを判定する。

        Returns:
            ローカル環境の場合はTrue

        """
        return (
            Environment(os.environ.get("ENVIRONMENT", Environment.LOCAL))
            == Environment.LOCAL
        )
