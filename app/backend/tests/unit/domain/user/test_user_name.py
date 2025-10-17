"""UserName値オブジェクトのユニットテスト。

ユーザー名値オブジェクトの動作をテストする。
"""

import pytest

from src.domain.user.name import UserName


class TestInit:
    """UserNameの初期化テストクラス。

    ユーザー名値オブジェクトの生成とバリデーションをテストする。
    """

    def test_OK_生成できること(self) -> None:
        # arrange
        name = "テストユーザネーム"

        # act
        result = UserName(name)

        # assert
        assert isinstance(result, UserName)
        assert result.value == name

    @pytest.mark.parametrize(
        ("name", "expected"),
        [
            pytest.param("", False, id="0文字"),
            pytest.param("a" * 1, True, id="1文字"),
            pytest.param("a" * 100, True, id="100文字"),
            pytest.param("a" * 101, False, id="101文字"),
        ],
    )
    def test_ユーザー名が1文字以上100文字以下であること(
        self,
        name: str,
        expected: bool,
    ) -> None:
        # act & assert
        if expected:
            UserName(name)
        else:
            with pytest.raises(ValueError):
                UserName(name)
