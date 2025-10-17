"""ログ設定の管理。

アプリケーション全体のログ設定とCloud Logging対応を行う。
"""

import inspect
import logging
import os
from enum import Enum

import structlog
from structlog.contextvars import merge_contextvars
from structlog.processors import JSONRenderer, TimeStamper, format_exc_info
from structlog.stdlib import BoundLogger, LoggerFactory, ProcessorFormatter
from structlog.typing import EventDict, Processor

from src.environment import Environment

"""
このシステムでは下記のログレベルとルールで運用を行う。

DEBUG:   特にルールはなく、開発者が自由に使う。本番では出力しない。
INFO:    運用時に見たいときに見る。
WARNING: 確認が必要な警告。勤務時間中はすぐ確認することもあるが、1営業日くらいの猶予があっていい。
ERROR:   即座に対応が必要なエラー。Slackに通知し、時間問わずに対応を行う。

ref. https://speakerdeck.com/irof/yi-li-turokuniqu-rizu-mou?slide=96
"""


class LogLevel(str, Enum):
    """ログレベルの定義。

    アプリケーションで使用するログレベルを定義する。
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    EXCEPTION = "ERROR"  # noqa: PIE796


def set_severity_level(
    _: BoundLogger,
    method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """Cloud Logging互換のseverityフィールドを付与する関数。
    method_nameには"info", "warning", "error"などが入り、それを大文字化して"INFO", "WARNING", "ERROR"といった
    Cloud Loggingが理解できるseverityとする。
    event_dict["severity"]が想定ログレベル外ならエラーを発生させる。
    """
    method_name = method_name.upper()
    # exceptionメソッドの場合はERRORとして扱う
    if method_name == "EXCEPTION":
        event_dict["severity"] = "ERROR"
    else:
        event_dict["severity"] = method_name
    log_level = LogLevel(event_dict["severity"])
    if log_level not in LogLevel:
        raise ValueError(f"Invalid method_name: {event_dict['severity']}")
    return event_dict


def drop_color_message_key(
    _: BoundLogger,
    __: str,
    event_dict: EventDict,
) -> EventDict:
    """Uvicornが`color_message`キーでメッセージを重複して記録することがあるため、
    不要な`color_message`キーを削除する関数。
    """
    event_dict.pop("color_message", None)
    return event_dict


def rename_event_to_message(
    _: BoundLogger,
    __: str,
    event_dict: EventDict,
) -> EventDict:
    """structlogはデフォルトでログメッセージを`event`キーに格納する。
    Cloud Loggingでは`message`キーが推奨されるため、`event`を`message`へリネームする関数。
    """
    event = event_dict.pop("event", None)
    if event is not None:
        event_dict["message"] = event
    return event_dict


def add_service_context(
    _: BoundLogger,
    __: str,
    event_dict: EventDict,
) -> EventDict:
    """Google Cloud Error Reportingとの統合に有用な`serviceContext`フィールドを追加する関数。
    Cloud Run環境変数 `K_SERVICE`や`K_REVISION`を用いてサービス名やバージョンを設定する。
    """
    service = os.environ.get("K_SERVICE", "unknown_service")
    revision = os.environ.get("K_REVISION", "unknown_revision")
    event_dict["serviceContext"] = {"service": service, "version": revision}
    return event_dict


def exception_to_stack_trace(
    _: BoundLogger,
    __: str,
    event_dict: EventDict,
) -> EventDict:
    """`format_exc_info`で`exception`キーとしてスタックトレースが生成されるが、
    Cloud LoggingとError Reporting連携で推奨される`stack_trace`キーに移し替える関数。
    """
    if "exception" in event_dict:
        event_dict["stack_trace"] = event_dict.pop("exception")
    return event_dict


def add_source_location(
    _: BoundLogger,
    __: str,
    event_dict: EventDict,
) -> EventDict:
    """ログが発生したソースコード位置を`logging.googleapis.com/sourceLocation`キールドに追記する関数。
    `inspect.stack()`を利用し、`site-packages`や`infrastructure/logging`ディレクトリを除外して、初めに発見したユーザーコード由来のフレームをソースとして採用する。
    """
    stack = inspect.stack()
    for frame_info in stack:
        filename = frame_info.filename
        if "site-packages" in filename:
            continue
        if "infrastructure/logging" in filename:
            continue
        event_dict["logging.googleapis.com/sourceLocation"] = {
            "file": filename,
            "line": str(frame_info.lineno),
            "function": frame_info.function,
        }
        break
    return event_dict


def setup_logging() -> None:
    """structlogによるロガーのセットアップを行う。

    環境に応じたログ設定とCloud Logging対応を行う。
    """
    shared_processors: list[Processor] = [
        merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        drop_color_message_key,
        set_severity_level,
        rename_event_to_message,
        TimeStamper(fmt="iso", key="time"),
        format_exc_info,
        exception_to_stack_trace,
    ]

    # 環境がローカルでない場合はソースロケーションやサービスコンテキストを追加
    if not Environment.is_local():
        shared_processors.append(add_source_location)
        shared_processors.append(add_service_context)

    # rendererの設定。ローカル環境ではコンソールレンダリング、それ以外ではJSON
    renderer: Processor
    if Environment.is_local():
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = JSONRenderer()

    # structlogのconfigure。ここでprocessorsにshared_processorsを仕込み、最後にrendererを入れる
    structlog.configure(
        processors=[*shared_processors, renderer],
        context_class=dict,
        wrapper_class=None,
        cache_logger_on_first_use=True,
        logger_factory=LoggerFactory(),
    )

    # 環境ごとにログレベルを設定
    if Environment.is_staging():
        log_level = LogLevel.INFO
    elif Environment.is_production():
        log_level = LogLevel.ERROR
    else:
        log_level = LogLevel.DEBUG

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level.value)

    # ここからProcessorFormatterを利用して、標準のloggingハンドラ経由のログもstructlogフォーマットへ
    # foreign_pre_chainにshared_processorsを指定することで、外部ライブラリの標準ログにもprocessorsを適用
    formatter = ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    # 標準出力にログを送るStreamHandlerを追加し、ProcessorFormatterをセット
    handler = logging.StreamHandler()
    handler.setLevel("INFO")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # uvicornのロガーのハンドラをクリアし、structlog経由で出力されるようにする
    for uvicorn_logger_name in ["uvicorn", "uvicorn.error"]:
        uvicorn_logger = logging.getLogger(uvicorn_logger_name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True

    # アクセスログのハンドラをクリア(アクセスログは別管理)
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.handlers.clear()
    access_logger.propagate = False


setup_logging()
logger: BoundLogger = structlog.get_logger()
