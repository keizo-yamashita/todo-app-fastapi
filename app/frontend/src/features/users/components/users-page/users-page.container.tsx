'use client'

import { useState, useEffect } from 'react'
import { User, UsersResponse, CreateUserRequest } from '@/types/user'
import { ApiError } from '@/types/api'
import { getUsers, createUser, deleteUser } from '@/lib/api-client'
import { UsersPage } from './users-page'

/**
 * ユーザーページ Containerコンポーネント
 *
 * データ取得、状態管理、ビジネスロジックを担当する
 *
 * @returns ユーザーページコンテナコンポーネント
 */
export function UsersPageContainer() {
  const [users, setUsers] = useState<User[]>([])
  const [pagination, setPagination] = useState<UsersResponse['pagination']>({
    page: 1,
    page_size: 10,
    total: 0,
    total_pages: 0,
  })
  const [currentPage, setCurrentPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [deletingId, setDeletingId] = useState<string | undefined>()

  /**
   * ユーザー一覧を取得する
   *
   * @param page ページ番号
   */
  const fetchUsers = async (page: number) => {
    try {
      setLoading(true)
      setError(null)
      const response = await getUsers(page, 10)
      setUsers(response.users)
      setPagination(response.pagination)
      setCurrentPage(page)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`${err.message} (${err.code})`)
      } else {
        setError('ユーザー一覧の取得に失敗しました')
      }
    } finally {
      setLoading(false)
    }
  }

  /**
   * ユーザーを作成する
   *
   * @param data ユーザー作成データ
   */
  const handleCreateUser = async (data: CreateUserRequest) => {
    try {
      setIsSubmitting(true)
      setError(null)
      await createUser(data)
      // 作成後、最初のページを再取得
      await fetchUsers(1)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`${err.message} (${err.code})`)
      } else {
        setError('ユーザーの作成に失敗しました')
      }
      throw err
    } finally {
      setIsSubmitting(false)
    }
  }

  /**
   * ユーザーを削除する
   *
   * @param id ユーザーID
   */
  const handleDeleteUser = async (id: string) => {
    if (!confirm('本当に削除しますか？')) {
      return
    }

    try {
      setDeletingId(id)
      setError(null)
      await deleteUser(id)

      // 削除後、現在のページを再取得
      // 現在のページにユーザーが1人しかいない場合は前のページに戻る
      if (users.length === 1 && currentPage > 1) {
        await fetchUsers(currentPage - 1)
      } else {
        await fetchUsers(currentPage)
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`${err.message} (${err.code})`)
      } else {
        setError('ユーザーの削除に失敗しました')
      }
    } finally {
      setDeletingId(undefined)
    }
  }

  /**
   * ページ変更ハンドラ
   *
   * @param page ページ番号
   */
  const handlePageChange = (page: number) => {
    fetchUsers(page)
  }

  /**
   * エラークリアハンドラ
   */
  const handleErrorClose = () => {
    setError(null)
  }

  // 初回レンダリング時にユーザー一覧を取得
  useEffect(() => {
    fetchUsers(1)
  }, [])

  return (
    <UsersPage
      users={users}
      pagination={pagination}
      loading={loading}
      error={error}
      onErrorClose={handleErrorClose}
      onCreateUser={handleCreateUser}
      isSubmitting={isSubmitting}
      onDeleteUser={handleDeleteUser}
      deletingId={deletingId}
      onPageChange={handlePageChange}
    />
  )
}
