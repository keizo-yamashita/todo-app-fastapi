'use client'

import { FormEvent } from 'react'
import { UserRole } from '@/types/user'
import styles from './user-form.module.css'

/**
 * ユーザーフォームのプロパティ
 */
interface UserFormProps {
  /** 名前の値 */
  name: string
  /** 名前変更時のコールバック */
  onNameChange: (name: string) => void
  /** メールアドレスの値 */
  email: string
  /** メールアドレス変更時のコールバック */
  onEmailChange: (email: string) => void
  /** ロールの値 */
  role: UserRole
  /** ロール変更時のコールバック */
  onRoleChange: (role: UserRole) => void
  /** フォーム送信時のコールバック */
  onSubmit: (e: FormEvent<HTMLFormElement>) => void
  /** 送信中かどうか */
  isSubmitting: boolean
}

/**
 * ユーザーフォーム Presentationコンポーネント
 *
 * ユーザー作成フォームのUIを提供する（純粋な表示のみ）
 *
 * @param props コンポーネントのプロパティ
 * @returns ユーザーフォームコンポーネント
 */
export function UserForm({
  name,
  onNameChange,
  email,
  onEmailChange,
  role,
  onRoleChange,
  onSubmit,
  isSubmitting,
}: UserFormProps) {
  return (
    <form className={styles.form} onSubmit={onSubmit}>
      <div className={styles.formGroup}>
        <label htmlFor="name" className={styles.label}>
          名前 <span className={styles.required}>*</span>
        </label>
        <input
          id="name"
          type="text"
          className={styles.input}
          value={name}
          onChange={(e) => onNameChange(e.target.value)}
          required
          minLength={1}
          maxLength={100}
          placeholder="山田 太郎"
          disabled={isSubmitting}
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="email" className={styles.label}>
          メールアドレス <span className={styles.required}>*</span>
        </label>
        <input
          id="email"
          type="email"
          className={styles.input}
          value={email}
          onChange={(e) => onEmailChange(e.target.value)}
          required
          placeholder="yamada@example.com"
          disabled={isSubmitting}
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="role" className={styles.label}>
          ロール <span className={styles.required}>*</span>
        </label>
        <select
          id="role"
          className={styles.select}
          value={role}
          onChange={(e) => onRoleChange(e.target.value as UserRole)}
          required
          disabled={isSubmitting}
        >
          <option value="user">ユーザー</option>
          <option value="admin">管理者</option>
        </select>
      </div>

      <button
        type="submit"
        className={styles.submitButton}
        disabled={isSubmitting}
      >
        {isSubmitting ? '作成中...' : 'ユーザーを作成'}
      </button>
    </form>
  )
}
