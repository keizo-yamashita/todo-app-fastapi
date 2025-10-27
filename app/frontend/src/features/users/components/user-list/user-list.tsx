'use client'

import { User } from '@/types/user'
import styles from './user-list.module.css'

/**
 * ユーザーリストのプロパティ
 */
interface UserListProps {
  /** ユーザーリスト */
  users: User[]
  /** ユーザー削除時のコールバック */
  onDelete: (id: string) => void
  /** 削除中のユーザーID */
  deletingId?: string
}

/**
 * ユーザーリスト Presentationコンポーネント
 *
 * ユーザー一覧を表示し、削除操作のUIを提供する（純粋な表示のみ）
 *
 * @param props コンポーネントのプロパティ
 * @returns ユーザーリストコンポーネント
 */
export function UserList({ users, onDelete, deletingId }: UserListProps) {
  if (users.length === 0) {
    return (
      <div className={styles.empty}>
        <p>ユーザーが登録されていません</p>
      </div>
    )
  }

  return (
    <div className={styles.container}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>ID</th>
            <th>名前</th>
            <th>メールアドレス</th>
            <th>ロール</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td className={styles.idCell}>{user.id}</td>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>
                <span className={styles.roleBadge} data-role={user.role}>
                  {user.role === 'admin' ? '管理者' : 'ユーザー'}
                </span>
              </td>
              <td>
                <button
                  className={styles.deleteButton}
                  onClick={() => onDelete(user.id)}
                  disabled={deletingId === user.id}
                  aria-label={`${user.name}を削除`}
                >
                  {deletingId === user.id ? '削除中...' : '削除'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
