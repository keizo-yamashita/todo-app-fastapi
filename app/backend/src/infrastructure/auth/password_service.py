"""パスワードハッシュ化サービス。

bcryptを使用したパスワードのハッシュ化と検証を提供する。
"""

import bcrypt

from src.domain.auth.password_hash import PasswordHash


class PasswordService:
    """パスワードハッシュ化サービス。

    パスワードのハッシュ化と検証機能を提供する。
    """

    @staticmethod
    def hash_password(plain_password: str) -> PasswordHash:
        """平文パスワードをハッシュ化する。

        Args:
            plain_password: 平文パスワード

        Returns:
            ハッシュ化されたパスワード

        """
        # パスワードをバイト列に変換
        password_bytes = plain_password.encode("utf-8")
        # bcryptでハッシュ化
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        # バイト列を文字列に変換して返す
        return PasswordHash(value=hashed.decode("utf-8"))

    @staticmethod
    def verify_password(plain_password: str, password_hash: PasswordHash) -> bool:
        """パスワードを検証する。

        Args:
            plain_password: 検証する平文パスワード
            password_hash: 保存されているパスワードハッシュ

        Returns:
            パスワードが一致する場合True

        """
        # パスワードとハッシュをバイト列に変換
        password_bytes = plain_password.encode("utf-8")
        hash_bytes = password_hash.value.encode("utf-8")
        # bcryptで検証
        return bcrypt.checkpw(password_bytes, hash_bytes)
