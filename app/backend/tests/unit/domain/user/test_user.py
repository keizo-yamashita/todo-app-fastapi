"""Userエンティティのユニットテスト。

ユーザーエンティティの動作をテストする。
"""

from datetime import datetime

from src.domain.user.email_address import EmailAddress
from src.domain.user.id import UserId
from src.domain.user.name import UserName
from src.domain.user.role import Role, RoleEnum
from src.domain.user.user import User


class TestInit:
    """Userの初期化テストクラス。

    ユーザーエンティティの生成とデフォルト値をテストする。
    """

    def test_OK_生成できること(self) -> None:
        # arrange
        user_id = UserId()
        email = EmailAddress.random()
        role = Role()
        name = UserName.random()

        # act
        user = User(
            id=user_id,
            email=email,
            role=role,
            name=name,
        )

        # assert
        assert isinstance(user, User)

    def test_OK_各値が渡されない場合はデフォルト値が設定されること(self) -> None:
        # arrange
        email = EmailAddress.random()

        # act
        user = User(email=email, name=UserName(value="test_name"))

        # assert
        assert user.role == Role()
        assert isinstance(user.id, UserId)
        assert isinstance(user.created_at, datetime)

    def test_OK_ユーザーの等価性比較が正しく動作すること(self) -> None:
        # arrange
        user_id = UserId(value="same-id")
        user1 = User(
            id=user_id,
            email=EmailAddress.random(),
            name=UserName(value="User 1"),
        )
        user2 = User(
            id=user_id,
            email=EmailAddress.random(),
            name=UserName(value="User 2"),
        )
        user3 = User(
            id=UserId(value="different-id"),
            email=EmailAddress.random(),
            name=UserName(value="User 3"),
        )

        # act & assert
        assert user1 == user2  # 同じIDなので等しい
        assert user1 != user3  # 異なるIDなので等しくない
        assert user1 != "not a user"  # 異なる型なので等しくない

    def test_OK_ユーザーのハッシュ値が正しく計算されること(self) -> None:
        # arrange
        user_id = UserId(value="test-id")
        user1 = User(
            id=user_id,
            email=EmailAddress.random(),
            name=UserName(value="User 1"),
        )
        user2 = User(
            id=user_id,
            email=EmailAddress.random(),
            name=UserName(value="User 2"),
        )

        # act & assert
        assert hash(user1) == hash(user2)  # 同じIDなので同じハッシュ値
        assert hash(user1) == hash(
            user_id
        )  # ユーザーのハッシュ値はIDのハッシュ値と同じ

    def test_OK_randomメソッドでランダムユーザーを生成できること(self) -> None:
        # act
        user = User.random()

        # assert
        assert isinstance(user, User)
        assert isinstance(user.email, EmailAddress)
        assert isinstance(user.name, UserName)
        assert isinstance(user.role, Role)

    def test_OK_randomメソッドでロールと名前を指定できること(self) -> None:
        # arrange
        custom_role = Role(value=RoleEnum.ADMIN)
        custom_name = UserName(value="Custom Name")

        # act
        user = User.random(role=custom_role, name=custom_name)

        # assert
        assert user.role == custom_role
        assert user.name == custom_name
        assert isinstance(user.email, EmailAddress)
