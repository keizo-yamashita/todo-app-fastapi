'use client'

import { User, Pagination as PaginationType } from '@/types/user'
import { UserList } from '../user-list'
import { UserFormContainer } from '../user-form/user-form.container'
import { Pagination } from '@/components/pagination'
import { ErrorMessage } from '@/components/error-message'
import styles from './users-page.module.css'

/**
 * ユーザーページのプロパティ
 */
interface UsersPageProps {
  /** ユーザーリスト */
  users: User[]
  /** ページネーション情報 */
  pagination: PaginationType
  /** 読み込み中かどうか */
  loading: boolean
  /** エラーメッセージ */
  error: string | null
  /** エラークリア時のコールバック */
  onErrorClose: () => void
  /** ユーザー作成時のコールバック */
  onCreateUser: (data: {
    name: string
    email: string
    role: 'user' | 'admin'
  }) => Promise<void>
  /** 作成中かどうか */
  isSubmitting: boolean
  /** ユーザー削除時のコールバック */
  onDeleteUser: (id: string) => void
  /** 削除中のユーザーID */
  deletingId?: string
  /** ページ変更時のコールバック */
  onPageChange: (page: number) => void
}

/**
 * ユーザーページ Presentationコンポーネント
 *
 * ユーザー管理画面全体のUIを提供する（純粋な表示のみ）
 *
 * @param props コンポーネントのプロパティ
 * @returns ユーザーページコンポーネント
 */
export function UsersPage({
  users,
  pagination,
  loading,
  error,
  onErrorClose,
  onCreateUser,
  isSubmitting,
  onDeleteUser,
  deletingId,
  onPageChange,
}: UsersPageProps) {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>ユーザー管理</h1>
        <p className={styles.description}>
          ユーザーの一覧表示、作成、削除ができます
        </p>
      </header>

      <main className={styles.main}>
        {error && <ErrorMessage message={error} onClose={onErrorClose} />}

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>新規ユーザー作成</h2>
          <UserFormContainer
            onSubmit={onCreateUser}
            isSubmitting={isSubmitting}
          />
        </section>

        <section className={styles.section}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>ユーザー一覧</h2>
            {!loading && (
              <span className={styles.totalCount}>
                全 {pagination.total} 件
              </span>
            )}
          </div>

          {loading ? (
            <div className={styles.loading}>読み込み中...</div>
          ) : (
            <>
              <UserList
                users={users}
                onDelete={onDeleteUser}
                deletingId={deletingId}
              />
              <Pagination pagination={pagination} onPageChange={onPageChange} />
            </>
          )}
        </section>
      </main>
    </div>
  )
}
