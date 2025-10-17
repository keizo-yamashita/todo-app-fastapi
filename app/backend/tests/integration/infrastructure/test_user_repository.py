"""ユーザーリポジトリの統合テスト。

PostgreSQLを使用したユーザーリポジトリの統合テストを行う。
"""

from dataclasses import replace
from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.email_address import EmailAddress
from src.domain.user.id import UserId
from src.domain.user.name import UserName
from src.domain.user.role import Role, RoleEnum
from src.domain.user.user import User
from src.infrastructure.repository.user.user_repository_impl import (
    UserRepositoryImpl,
)
from src.shared.errors.codes import (
    UserErrorCode,
)
from src.shared.errors.errors import (
    ExpectedBusinessError,
)


@pytest.fixture
def mock_user_repository(db_session: AsyncSession) -> UserRepositoryImpl:
    """テスト用のユーザーリポジトリを提供する。

    Args:
        db_session: データベースセッション

    Returns:
        UserRepositoryImpl: ユーザーリポジトリ

    """
    return UserRepositoryImpl(session=db_session)


class TestFilterUser:
    """ユーザー一覧取得のテストクラス。

    複数のユーザーを保存して一覧取得の動作をテストする。
    """

    @pytest.mark.anyio
    async def test_OK(self, mock_user_repository: UserRepositoryImpl) -> None:
        # arrange
        # テスト用のユーザーを3パターン用意
        test_user_num = 3
        test_users = []
        for _ in range(test_user_num):
            user = User(
                id=UserId(),
                email=EmailAddress.random(),
                role=Role(value=RoleEnum.MEMBER),
                name=UserName(value="test_name"),
            )
            test_users.append(user)
            await mock_user_repository.save(user)

        # act
        users = await mock_user_repository.filter()

        # assert
        assert len(users) == test_user_num
        test_user_ids = [test_user.id.value for test_user in test_users]
        for user in users:
            assert user.id.value in test_user_ids


class TestFindUser:
    """ユーザーID検索のテストクラス。

    IDでユーザーを検索する動作をテストする。
    """

    @pytest.mark.anyio
    async def test_OK_ユーザーが見つかること(
        self,
        mock_user_repository: UserRepositoryImpl,
    ) -> None:
        # arrange
        test_user = User(
            id=UserId(),
            email=EmailAddress.random(),
            role=Role(value=RoleEnum.MEMBER),
            name=UserName(value="test_name"),
        )
        await mock_user_repository.save(test_user)

        # act
        found = await mock_user_repository.find_by_id(test_user.id)

        # assert
        assert found.created_at is not None
        dummy_time = datetime(2000, 1, 1, tzinfo=UTC)
        assert replace(found, created_at=dummy_time) == replace(
            test_user,
            created_at=dummy_time,
        )

    @pytest.mark.anyio
    async def test_NG_ユーザーが見つからなかった場合例外を返すこと(
        self,
        mock_user_repository: UserRepositoryImpl,
    ) -> None:
        # arrange
        user_id = UserId()

        # act & assert
        with pytest.raises(ExpectedBusinessError) as e:
            await mock_user_repository.find_by_id(user_id)
        assert e.value.details == {"user_id": user_id.value}
        assert e.value.code == UserErrorCode.NotFound


class TestFindByEmailUser:
    """メールアドレス検索のテストクラス。

    メールアドレスでユーザーを検索する動作をテストする。
    """

    @pytest.mark.anyio
    async def test_OK(self, mock_user_repository: UserRepositoryImpl) -> None:
        # arrange
        user_id = UserId()
        user = User(
            id=user_id,
            email=EmailAddress.random(),
            role=Role(value=RoleEnum.MEMBER),
            name=UserName(value="test_name"),
        )
        await mock_user_repository.save(user)

        # act
        found = await mock_user_repository.find_by_email(user.email)

        # assert
        assert found.created_at is not None
        dummy_time = datetime(2000, 1, 1, tzinfo=UTC)
        assert replace(found, created_at=dummy_time) == replace(
            user,
            created_at=dummy_time,
        )

    @pytest.mark.anyio
    async def test_NG_ユーザーが見つからなかった場合ビジネス例外を返すこと(
        self,
        mock_user_repository: UserRepositoryImpl,
    ) -> None:
        # arrange
        email = EmailAddress.random()

        # act & assert
        with pytest.raises(ExpectedBusinessError) as e:
            await mock_user_repository.find_by_email(email)
        assert e.value.details == {"email": email.value}
        assert e.value.code == UserErrorCode.NotFound


class TestSaveUser:
    """ユーザー保存のテストクラス。

    ユーザーをデータベースに保存する動作をテストする。
    """

    @pytest.mark.anyio
    async def test_OK(self, mock_user_repository: UserRepositoryImpl) -> None:
        # arrange
        user_id = UserId()
        user = User(
            id=user_id,
            email=EmailAddress.random(),
            role=Role(value=RoleEnum.MEMBER),
            name=UserName(value="test_name"),
        )

        # act
        saved = await mock_user_repository.save(user)

        # assert
        assert saved == user

    @pytest.mark.anyio
    async def test_NG_既にEmailが存在する場合技術的な例外を返すこと(
        self,
        mock_user_repository: UserRepositoryImpl,
    ) -> None:
        # arrange
        user = User(
            id=UserId(),
            email=EmailAddress.random(),
            role=Role(value=RoleEnum.MEMBER),
            name=UserName(value="test_name"),
        )
        await mock_user_repository.save(user)
        duplicate_user = User(
            id=UserId(),
            email=user.email,
            role=Role(value=RoleEnum.MEMBER),
            name=UserName(value="test_name"),
        )

        # act & assert
        with pytest.raises(ExpectedBusinessError) as e:
            await mock_user_repository.save(duplicate_user)
        assert e.value.details == {"email": duplicate_user.email.value}
        assert e.value.code == UserErrorCode.EmailAlreadyExists


class TestDeleteUser:
    """ユーザー削除のテストクラス。

    ユーザーをデータベースから削除する動作をテストする。
    """

    @pytest.mark.anyio
    async def test_OK(self, mock_user_repository: UserRepositoryImpl) -> None:
        # arrange
        user_id = UserId()
        user = User(
            id=user_id,
            email=EmailAddress.random(),
            role=Role(value=RoleEnum.MEMBER),
            name=UserName(value="test_name"),
        )
        await mock_user_repository.save(user)

        # act
        returned_user_id = await mock_user_repository.delete(user_id)

        # assert
        assert user_id.value == returned_user_id.value

        # 物理削除されているので、find_by_idで見つからずエラーが発生する
        with pytest.raises(ExpectedBusinessError) as e:
            await mock_user_repository.find_by_id(user_id)
        assert e.value.code == UserErrorCode.NotFound

    @pytest.mark.anyio
    async def test_NG_存在しないユーザIDを指定した場合UserNotFoundErrorが返ること(
        self,
        mock_user_repository: UserRepositoryImpl,
    ) -> None:
        # arrange
        user_id = UserId()

        # act & assert
        with pytest.raises(ExpectedBusinessError) as e:
            await mock_user_repository.delete(user_id)
        assert e.value.details == {"user_id": user_id.value}
        assert e.value.code == UserErrorCode.NotFound
