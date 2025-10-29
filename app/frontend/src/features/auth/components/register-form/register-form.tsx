/**
 * 新規登録フォームのPresentationコンポーネント
 */

import Link from 'next/link'

import styles from './register-form.module.css'

interface RegisterFormProps {
  /**
   * メールアドレス
   */
  email: string
  /**
   * 名前
   */
  name: string
  /**
   * パスワード
   */
  password: string
  /**
   * パスワード確認
   */
  passwordConfirm: string
  /**
   * 送信中かどうか
   */
  isSubmitting: boolean
  /**
   * エラーメッセージ
   */
  error: string | null
  /**
   * メールアドレス変更ハンドラー
   */
  onEmailChange: (email: string) => void
  /**
   * 名前変更ハンドラー
   */
  onNameChange: (name: string) => void
  /**
   * パスワード変更ハンドラー
   */
  onPasswordChange: (password: string) => void
  /**
   * パスワード確認変更ハンドラー
   */
  onPasswordConfirmChange: (passwordConfirm: string) => void
  /**
   * 送信ハンドラー
   */
  onSubmit: (e: React.FormEvent) => void
}

/**
 * 新規登録フォームのPresentationコンポーネント
 */
export const RegisterForm = ({
  email,
  name,
  password,
  passwordConfirm,
  isSubmitting,
  error,
  onEmailChange,
  onNameChange,
  onPasswordChange,
  onPasswordConfirmChange,
  onSubmit,
}: RegisterFormProps) => {
  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={onSubmit}>
        <h1 className={styles.title}>新規登録</h1>

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
          <label htmlFor="name" className={styles.label}>
            名前
          </label>
          <input
            type="text"
            id="name"
            className={styles.input}
            value={name}
            onChange={(e) => {
              onNameChange(e.target.value)
            }}
            onInvalid={(e) => {
              const target = e.target as HTMLInputElement
              if (target.validity.valueMissing) {
                target.setCustomValidity('名前を入力してください')
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
              } else if (target.validity.tooShort) {
                target.setCustomValidity(
                  'パスワードは8文字以上で入力してください'
                )
              }
            }}
            onInput={(e) => {
              const target = e.target as HTMLInputElement
              target.setCustomValidity('')
            }}
            required={true}
            disabled={isSubmitting}
            minLength={8}
          />
          <p className={styles.hint}>8文字以上で入力してください</p>
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="passwordConfirm" className={styles.label}>
            パスワード（確認）
          </label>
          <input
            type="password"
            id="passwordConfirm"
            className={styles.input}
            value={passwordConfirm}
            onChange={(e) => {
              onPasswordConfirmChange(e.target.value)
            }}
            onInvalid={(e) => {
              const target = e.target as HTMLInputElement
              if (target.validity.valueMissing) {
                target.setCustomValidity('パスワード（確認）を入力してください')
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
          {isSubmitting ? '登録中...' : '登録'}
        </button>

        <div className={styles.loginLink}>
          <Link href="/login">ログインはこちら</Link>
        </div>
      </form>
    </div>
  )
}
