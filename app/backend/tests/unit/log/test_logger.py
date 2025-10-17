"""ログ設定のユニットテスト。

ログ設定機能の動作をテストする。
"""

import os
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest

if TYPE_CHECKING:
    from structlog.types import EventDict

from src.log.logger import (
    LogLevel,
    add_service_context,
    add_source_location,
    drop_color_message_key,
    exception_to_stack_trace,
    rename_event_to_message,
    set_severity_level,
)


class TestLogLevel:
    """LogLevelのテストクラス。

    ログレベルの定義をテストする。
    """

    def test_OK_LogLevelの値が正しく定義されていること(self) -> None:
        assert LogLevel.DEBUG == "DEBUG"
        assert LogLevel.INFO == "INFO"
        assert LogLevel.WARNING == "WARNING"
        assert LogLevel.ERROR == "ERROR"
        assert LogLevel.EXCEPTION == "ERROR"


class TestSetSeverityLevel:
    """SetSeverityLevelのテストクラス。

    ログの重要度レベル設定機能をテストする。
    """

    @pytest.mark.parametrize(
        ("method_name", "expected_severity"),
        [
            pytest.param("info", "INFO", id="INFOレベル"),
            pytest.param("warning", "WARNING", id="WARNINGレベル"),
            pytest.param("error", "ERROR", id="ERRORレベル"),
            pytest.param("exception", "ERROR", id="EXCEPTIONレベル"),
        ],
    )
    def test_OK_各ログレベルが正しく設定されること(
        self,
        method_name: str,
        expected_severity: str,
    ) -> None:
        """各ログレベルが正しく設定されること"""
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {}

        # act
        result = set_severity_level(logger_mock, method_name, event_dict)

        # assert
        assert result["severity"] == expected_severity

    def test_NG_無効なログレベルでValueErrorが発生すること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {}

        # act & assert
        with pytest.raises(ValueError, match="is not a valid LogLevel"):
            set_severity_level(logger_mock, "invalid", event_dict)


class TestDropColorMessageKey:
    """DropColorMessageKeyのテストクラス。

    カラーメッセージキーの削除機能をテストする。
    """

    def test_OK_color_messageキーが削除されること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {
            "message": "test message",
            "color_message": "colored test message",
        }

        # act
        result = drop_color_message_key(logger_mock, "", event_dict)

        # assert
        assert "color_message" not in result
        assert result["message"] == "test message"

    def test_OK_color_messageキーが存在しない場合も正常に動作すること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {"message": "test message"}

        # act
        result = drop_color_message_key(logger_mock, "", event_dict)

        # assert
        assert result["message"] == "test message"


class TestRenameEventToMessage:
    """RenameEventToMessageのテストクラス。

    イベントキーをメッセージキーにリネームする機能をテストする。
    """

    def test_OK_eventキーがmessageキーにリネームされること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {"event": "test event"}

        # act
        result = rename_event_to_message(logger_mock, "", event_dict)

        # assert
        assert "event" not in result
        assert result["message"] == "test event"

    def test_OK_eventキーが存在しない場合も正常に動作すること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {"other": "value"}

        # act
        result = rename_event_to_message(logger_mock, "", event_dict)

        # assert
        assert "message" not in result
        assert result["other"] == "value"


class TestAddServiceContext:
    """AddServiceContextのテストクラス。

    サービスコンテキストの追加機能をテストする。
    """

    @patch.dict(
        os.environ,
        {"K_SERVICE": "test-service", "K_REVISION": "test-revision"},
    )
    def test_OK_環境変数からサービスコンテキストが追加されること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {}

        # act
        result = add_service_context(logger_mock, "", event_dict)

        # assert
        assert result["serviceContext"]["service"] == "test-service"
        assert result["serviceContext"]["version"] == "test-revision"

    @patch.dict(os.environ, {}, clear=True)
    def test_OK_環境変数が存在しない場合デフォルト値が設定されること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {}

        # act
        result = add_service_context(logger_mock, "", event_dict)

        # assert
        assert result["serviceContext"]["service"] == "unknown_service"
        assert result["serviceContext"]["version"] == "unknown_revision"


class TestExceptionToStackTrace:
    """ExceptionToStackTraceのテストクラス。

    例外をスタックトレースに変換する機能をテストする。
    """

    def test_OK_exceptionキーがstack_traceキーに移されること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {"exception": "test stack trace"}

        # act
        result = exception_to_stack_trace(logger_mock, "", event_dict)

        # assert
        assert "exception" not in result
        assert result["stack_trace"] == "test stack trace"

    def test_OK_exceptionキーが存在しない場合も正常に動作すること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {"other": "value"}

        # act
        result = exception_to_stack_trace(logger_mock, "", event_dict)

        # assert
        assert "stack_trace" not in result
        assert result["other"] == "value"


class TestAddSourceLocation:
    """AddSourceLocationのテストクラス。

    ソースロケーション情報の追加機能をテストする。
    """

    def test_OK_ソースロケーション情報が追加されること(self) -> None:
        # arrange
        logger_mock = Mock()
        event_dict: EventDict = {}

        # act
        result = add_source_location(logger_mock, "", event_dict)

        # assert
        assert "logging.googleapis.com/sourceLocation" in result
        location = result["logging.googleapis.com/sourceLocation"]
        assert "file" in location
        assert "line" in location
        assert "function" in location
        # 実際の関数名をチェック(この関数内で呼び出されているため)
        assert (
            "test_adds_source_location" in location["function"]
            or "add_source_location" in location["function"]
        )
