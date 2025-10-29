"""APIルートの定義。

ヘルスチェック、認証、ユーザー関連のエンドポイントを提供する。
"""

from fastapi import APIRouter

from src.presentation.api.routes.auth import router as auth_router
from src.presentation.api.routes.user import user_router
from src.presentation.api.schema.healthz.check_healthz import CheckHealthResponse

router = APIRouter()


@router.get(
    "/healthz",
    summary="Check Health",
    description="Check the health of the API",
    responses={200: {"model": CheckHealthResponse}},
)
async def check_health() -> CheckHealthResponse:
    """APIのヘルスチェックを行う。

    システムが正常に動作しているかを確認する。
    """
    return CheckHealthResponse(status="OK")


router.include_router(auth_router)
router.include_router(user_router)
