/**
 * APIエラーレスポンス
 */
export interface ApiErrorResponse {
  /** エラーコード */
  code: string
  /** エラーメッセージ */
  message: string
  /** 詳細情報（オプション） */
  details?: Record<string, unknown>
}

/**
 * APIエラークラス
 */
export class ApiError extends Error {
  /**
   * APIエラーを作成する
   *
   * @param status HTTPステータスコード
   * @param code エラーコード
   * @param message エラーメッセージ
   * @param details 詳細情報
   */
  constructor(
    public status: number,
    public code: string,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message)
    this.name = 'ApiError'
  }
}
