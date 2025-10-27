/**
 * 認証関連の型定義
 */

/**
 * 新規登録リクエスト
 */
export interface RegisterRequest {
  email: string
  name: string
  password: string
}

/**
 * 新規登録レスポンス
 */
export interface RegisterResponse {
  id: string
  email: string
  name: string
  role: string
}

/**
 * ログインリクエスト
 */
export interface LoginRequest {
  email: string
  password: string
}

/**
 * ユーザー情報
 */
export interface UserInfo {
  id: string
  email: string
  name: string
  role: string
}

/**
 * ログインレスポンス
 */
export interface LoginResponse {
  user: UserInfo
  access_token: string
  token_type: string
}
