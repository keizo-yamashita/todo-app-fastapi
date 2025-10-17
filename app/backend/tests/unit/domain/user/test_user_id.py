"""UserId値オブジェクトのユニットテスト。

ユーザーID値オブジェクトの動作をテストする。
"""

import uuid

from src.domain.user.id import UserId


class TestInit:
    """UserIdの初期化テストクラス。

    ユーザーID値オブジェクトの生成とデフォルト値をテストする。
    """

    def test_OK_生成できること(self) -> None:
        # arrange
        valid_uuid = str(uuid.uuid4())

        # act
        result = UserId(value=valid_uuid)

        # assert
        assert isinstance(result, UserId)
        assert result.value == valid_uuid

    def test_OK_idがNoneの場合はuuid4が生成されること(self) -> None:
        # act
        result = UserId()

        # assert
        assert isinstance(result, UserId)
        assert isinstance(result.value, str)
