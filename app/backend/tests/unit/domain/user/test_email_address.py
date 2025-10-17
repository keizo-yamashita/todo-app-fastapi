"""EmailAddressのユニットテスト。

メールアドレス値オブジェクトの動作をテストする。
"""

import pytest

from src.domain.user.email_address import EmailAddress


class TestInit:
    """EmailAddressの初期化テストクラス。

    メールアドレス値オブジェクトの生成とバリデーションをテストする。
    """

    def test_OK_生成できること(self) -> None:
        # arrange
        email_str = "test.account.dev@gmail.com"

        # act
        email = EmailAddress(email_str)

        # assert
        assert isinstance(email, EmailAddress)
        assert email.value == email_str

    def test_OK_ランダム生成できること(self) -> None:
        # arrange & when
        email = EmailAddress.random()

        # assert
        assert isinstance(email, EmailAddress)

    @pytest.mark.parametrize(
        ("email_address"),
        [
            pytest.param("", id="空文字"),
            pytest.param("invalid-email", id="@以降が空"),
            pytest.param("@example.com", id="ローカルパートが空"),
            pytest.param("test@", id="ドメインが空"),
            pytest.param("test@example", id="トップレベルドメインがない"),
            pytest.param("test@example..com", id="ドメイン内に連続したドット"),
            pytest.param("test.@example.com", id="ローカルパート末尾のドット"),
            pytest.param(".test@example.com", id="ローカルパート先頭のドット"),
            pytest.param(
                "test..test@example.com", id="ローカルパート内の連続したドット"
            ),
            pytest.param("test@example.com.", id="ドメイン末尾のドット"),
            pytest.param("te st@example.com", id="ローカルパート内のスペース"),
            pytest.param("test@exam ple.com", id="ドメイン内のスペース"),
            pytest.param("a" * 65 + "@example.com", id="長すぎるローカルパート"),
            pytest.param("test@" + "a" * 252 + ".com", id="長すぎるドメイン"),
        ],
    )
    def test_NG_フォーマットが不正な場合はValueErrorが投げられること(
        self,
        email_address: str,
    ) -> None:
        # act & assert
        with pytest.raises(ValueError):
            EmailAddress(email_address)
