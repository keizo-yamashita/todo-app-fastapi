import styles from './error-message.module.css'

/**
 * エラーメッセージコンポーネントのプロパティ
 */
interface ErrorMessageProps {
  /** エラーメッセージ */
  message: string
  /** 閉じるボタンのコールバック（オプション） */
  onClose?: () => void
}

/**
 * エラーメッセージ Presentationコンポーネント
 *
 * エラーメッセージを表示する汎用コンポーネント（純粋な表示のみ）
 *
 * @param props コンポーネントのプロパティ
 * @returns エラーメッセージコンポーネント
 */
export function ErrorMessage({ message, onClose }: ErrorMessageProps) {
  return (
    <div className={styles.container} role="alert">
      <div className={styles.content}>
        <span className={styles.icon}>⚠️</span>
        <span className={styles.message}>{message}</span>
      </div>
      {onClose && (
        <button
          className={styles.closeButton}
          onClick={onClose}
          aria-label="エラーメッセージを閉じる"
        >
          ×
        </button>
      )}
    </div>
  )
}
