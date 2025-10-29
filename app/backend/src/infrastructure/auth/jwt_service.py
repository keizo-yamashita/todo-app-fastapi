"""JWT生成・検証サービス。

python-jose[cryptography]を使用したJWTトークンの生成と検証を提供する。
"""

import os
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from src.domain.user.id import UserId
from src.shared.errors.codes import AuthErrorCode
from src.shared.errors.errors import ExpectedBusinessError

# JWT設定
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class JWTService:
    """JWT生成・検証サービス。

    JWTトークンの生成と検証機能を提供する。
    """

    @staticmethod
    def create_access_token(user_id: UserId) -> str:
        """アクセストークンを生成する。

        Args:
            user_id: ユーザーID

        Returns:
            JWTアクセストークン

        """
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": user_id.value,
            "exp": expire,
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> UserId:
        """トークンを検証しユーザーIDを取得する。

        Args:
            token: JWTトークン

        Returns:
            ユーザーID

        Raises:
            ExpectedBusinessError: トークンが無効または期限切れの場合

        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id_str: str | None = payload.get("sub")
            if user_id_str is None:
                raise ExpectedBusinessError(
                    code=AuthErrorCode.InvalidToken,
                )
            return UserId(value=user_id_str)
        except JWTError as e:
            raise ExpectedBusinessError(
                code=AuthErrorCode.InvalidToken,
            ) from e
