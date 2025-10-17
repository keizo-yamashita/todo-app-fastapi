"""FastAPIアプリケーションのメインエントリーポイント。

APIサーバーの設定、ミドルウェア、エラーハンドリングを定義する。
"""

import os
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

import structlog
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import Response

from src.environment import Environment
from src.infrastructure.config.database import close_db, init_db
from src.log.logger import logger
from src.presentation.api.routes.route import router
from src.presentation.api.schema.error_response import (
    ErrorResponse,
    ValidationErrorResponse,
)
from src.shared.errors.codes import CommonErrorCode
from src.shared.errors.errors import (
    ExpectedBusinessError,
    ExpectedUseCaseError,
)

# HTTPステータスコード定数
HTTP_SERVER_ERROR_THRESHOLD = 500

app = FastAPI(
    title="gg-template-fastapi-next",
    version="1.0.0",
    root_path="/api",
)

# CORSのミドルウェアを設定
allowed_origins = os.getenv("ALLOWED_ORIGIN", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ルーティングを設定
app.include_router(router)


# アプリケーション起動時のイベント
@app.on_event("startup")
async def startup_event() -> None:
    """アプリケーション起動時の処理。

    データベース接続の初期化などを行う。
    """
    logger.info(
        "Application startup", environment=os.environ.get("ENVIRONMENT", "local")
    )
    # 開発環境ではテーブルを自動作成(本番ではAlembicを使用)
    if Environment.is_local():
        await init_db()
        logger.info("Database tables initialized")


# アプリケーション終了時のイベント
@app.on_event("shutdown")
async def shutdown_event() -> None:
    """アプリケーション終了時の処理。

    データベース接続のクローズなどを行う。
    """
    logger.info("Application shutdown")
    await close_db()


# リクエスト・レスポンスのログを出力するミドルウェア
@app.middleware("http")
async def log_requests(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """リクエスト・レスポンスのログを出力するミドルウェア。

    リクエストの開始・完了・エラーをログに記録し、
    リクエストIDとトレースIDをコンテキストにバインドする。

    Args:
        request: HTTPリクエスト
        call_next: 次のミドルウェアまたはハンドラー

    Returns:
        HTTPレスポンス

    """
    # リクエストごとにコンテキストをバインド。これにより後続のログにコンテキストが追加される
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        trace_id=request.headers.get(
            "X-Cloud-Trace-Context",
        ),  # Cloud Runの場合はこれを使う
    )

    start_time = time.perf_counter()

    http_request_info = {
        "requestMethod": request.method,
        "requestUrl": str(request.url),
        "userAgent": request.headers.get("User-Agent"),
        "remoteIp": getattr(request.client, "host", None) if request.client else None,
        "protocol": request.scope.get("http_version", "HTTP/1.1"),
        "requestSize": request.headers.get("content-length", "0"),
    }

    # リクエスト開始ログ
    logger.info("request_started", httpRequest=http_request_info)

    try:
        response = await call_next(request)
    except Exception:
        duration = (time.perf_counter() - start_time) * 1000
        errored_request_info = {
            **http_request_info,
            "status": 500,
            "responseSize": "0",
        }
        logger.exception(
            "request_errored",
            httpRequest=errored_request_info,
            duration_ms=duration,
        )
        raise

    response_size = response.headers.get("content-length", "0")
    duration = (time.perf_counter() - start_time) * 1000

    completed_request_info = {
        **http_request_info,
        "status": response.status_code,
        "responseSize": response_size,
    }

    response.headers["X-Request-Id"] = request_id
    logger.info(
        "request_completed",
        httpRequest=completed_request_info,
        duration_ms=duration,
    )

    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Pydanticによるリクエストのバリデーションに失敗した場合に呼び出されるハンドラーです。
    Pydanticのバリデーションエラーを適切な形式のレスポンスに変換します。
    """
    errors_dict: dict[str, list[str]] = {}
    # Pydanticのエラー情報を直接処理
    for err in exc.errors():
        loc = tuple(str(loc_item) for loc_item in err.get("loc", ()))
        err_type = err.get("type", "")
        # "value_error.missing" のような場合、最後の要素をエラーコードとして使用
        error_code = err_type.split(".")[-1] if "." in err_type else err_type

        # locからfield_nameを生成
        field_name = ".".join(
            str(part)
            for part in loc
            if part not in ("body", "query", "path", "header", "cookie")
        )
        if not field_name:
            field_name = ".".join(str(location_part) for location_part in loc)

        errors_dict.setdefault(field_name, []).append(error_code)

    response_content: dict[str, Any] = {"errors": errors_dict}
    logger.info("validation_error", errors=errors_dict)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ValidationErrorResponse(**response_content).model_dump(),
    )


@app.exception_handler(ExpectedUseCaseError)
async def expected_usecase_error_fallback_handler(
    request: Request,
    exc: ExpectedUseCaseError,
) -> JSONResponse:
    """ExpectedUseCaseError のフォールバックハンドラー。

    注意: このハンドラーが呼ばれる場合、ルーターでの例外処理が漏れています。
    ExpectedUseCaseError は本来、各エンドポイントで適切なHTTPステータスに
    変換されるべきです。
    """
    logger.error(
        "ExpectedUseCaseErrorがルーターでハンドリングされていません。ルーターでの例外処理を確認してください。",
        error_code=exc.code,
        raw_message=exc.raw_message,
        details=exc.details,
        url=str(request.url),
        endpoint_path=request.url.path,
    )

    # 開発環境では例外を再レイズして問題を明確にする
    if Environment.is_local():
        raise RuntimeError(
            f"ExpectedUseCaseError was not handled in router: {request.url.path} "
            f"Error code: {exc.code} - Please handle this exception in the endpoint.",
        ) from exc

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            message=CommonErrorCode.UnexpectedError.value,
        ).model_dump(),
    )


@app.exception_handler(ExpectedBusinessError)
async def expected_business_error_handler(
    _: Request,
    exc: ExpectedBusinessError,
) -> JSONResponse:
    """注意点:
    基本的に予期するビジネスエラーはルーターでハンドリングしているが、
    Unauthorized(401)は依存性注入時に発生しルーターでハンドリングできないため例外的にここでハンドリングする
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=ErrorResponse(message=exc.code.value).model_dump(),
    )


@app.exception_handler(HTTPException)
async def global_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """グローバル例外ハンドラー。

    HTTPExceptionを処理し、適切なHTTPステータスコードと
    エラーメッセージを返す。

    Args:
        request: HTTPリクエスト
        exc: HTTPException

    Returns:
        JSONレスポンス

    """
    # HTTPExceptionの場合は元のステータスコードとメッセージを保持
    if exc.status_code < HTTP_SERVER_ERROR_THRESHOLD:
        # 4xx系のエラーは期待される例外なのでinfoレベルでログ
        logger.info(
            "HTTPException occurred",
            status_code=exc.status_code,
            detail=exc.detail,
            url=str(request.url),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(message=str(exc.detail)).model_dump(),
        )

    # 5xx系のエラーは予期しない例外なのでerrorレベルでログ
    logger.exception(
        "予期しないビジネス or 技術的エラーが発生しました。",
        detail=exc.detail,
        url=str(request.url),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            message=CommonErrorCode.UnexpectedError.value,
        ).model_dump(),
    )
