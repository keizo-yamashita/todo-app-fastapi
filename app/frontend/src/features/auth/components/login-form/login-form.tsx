/**
 * ログインフォームのPresentationコンポーネント
 */

import Link from 'next/link'
import styles from './login-form.module.css'

interface LoginFormProps {
  /**
   * メールアドレス
   */
  email: string
  /**
   * パスワード
   */
  password: string
  /**
   * 送信中かどうか
   */
  isSubmitting: boolean
  /**
   * エラーメッセージ
   */
  error: string | null
  /**
   * 成功メッセージ
   */
  successMessage: string | null
  /**
   * メールアドレス変更ハンドラー
   */
  onEmailChange: (email: string) => void
  /**
   * パスワード変更ハンドラー
   */
  onPasswordChange: (password: string) => void
  /**
   * 送信ハンドラー
   */
  onSubmit: (e: React.FormEvent) => void
}

/**
 * ログインフォームのPresentationコンポーネント
 */
export const LoginForm = ({
  email,
  password,
  isSubmitting,
  error,
  successMessage,
  onEmailChange,
  onPasswordChange,
  onSubmit,
}: LoginFormProps) => {
  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={onSubmit}>
        <h1 className={styles.title}>ログイン</h1>

        {successMessage !== null && (
          <div className={styles.success}>{successMessage}</div>
        )}

        {error !== null && <div className={styles.error}>{error}</div>}

        <div className={styles.formGroup}>
          <label htmlFor="email" className={styles.label}>
            メールアドレス
          </label>
          <input
            type="email"
            id="email"
            className={styles.input}
            value={email}
            onChange={(e) => {
              onEmailChange(e.target.value)
            }}
            onInvalid={(e) => {
              const target = e.target as HTMLInputElement
              if (target.validity.valueMissing) {
                target.setCustomValidity('メールアドレスを入力してください')
              } else if (target.validity.typeMismatch) {
                target.setCustomValidity(
                  'メールアドレスの形式が正しくありません'
                )
              }
            }}
            onInput={(e) => {
              const target = e.target as HTMLInputElement
              target.setCustomValidity('')
            }}
            required={true}
            disabled={isSubmitting}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="password" className={styles.label}>
            パスワード
          </label>
          <input
            type="password"
            id="password"
            className={styles.input}
            value={password}
            onChange={(e) => {
              onPasswordChange(e.target.value)
            }}
            onInvalid={(e) => {
              const target = e.target as HTMLInputElement
              if (target.validity.valueMissing) {
                target.setCustomValidity('パスワードを入力してください')
              }
            }}
            onInput={(e) => {
              const target = e.target as HTMLInputElement
              target.setCustomValidity('')
            }}
            required={true}
            disabled={isSubmitting}
          />
        </div>

        <button
          type="submit"
          className={styles.submitButton}
          disabled={isSubmitting}
        >
          {isSubmitting ? 'ログイン中...' : 'ログイン'}
        </button>

        <div className={styles.registerLink}>
          <Link href="/register">新規登録はこちら</Link>
        </div>
      </form>
    </div>
  )
}
