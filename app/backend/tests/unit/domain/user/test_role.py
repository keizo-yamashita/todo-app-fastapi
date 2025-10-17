"""Role値オブジェクトのユニットテスト。

ロール値オブジェクトの動作をテストする。
"""

import pytest

from src.domain.user.role import Role, RoleEnum


class TestInit:
    """Roleの初期化テストクラス。

    ロール値オブジェクトの生成とデフォルト値をテストする。
    """

    def test_OK_生成できること(self) -> None:
        # arrange
        role = RoleEnum.MEMBER

        # act
        result = Role(value=role)

        # assert
        assert isinstance(result, Role)
        assert result.value == role

    def test_OK_何も入力しない場合はmemberを返す(self) -> None:
        # act
        result = Role()

        # act & then
        assert isinstance(result, Role)
        assert result.value == RoleEnum.MEMBER

    def test_OK_各ロールを正しく生成できること(self) -> None:
        # arrange & act & assert
        superadmin_role = Role(value=RoleEnum.SUPERADMIN)
        assert superadmin_role.value == RoleEnum.SUPERADMIN

        admin_role = Role(value=RoleEnum.ADMIN)
        assert admin_role.value == RoleEnum.ADMIN

        member_role = Role(value=RoleEnum.MEMBER)
        assert member_role.value == RoleEnum.MEMBER

    def test_NG_無効な型を渡した場合はTypeErrorが投げられること(self) -> None:
        # act & assert
        with pytest.raises(TypeError) as e:
            Role(value="invalid_role")  # type: ignore[arg-type]

        assert "invalid role type" in str(e.value)
        assert "expected: RoleEnum" in str(e.value)

    def test_OK_DEFAULT_ROLE定数が正しく定義されていること(self) -> None:
        # assert
        assert Role.DEFAULT_ROLE == RoleEnum.MEMBER
