/**
 * ユーザーのロール
 */
export type UserRole = 'admin' | 'user'

/**
 * ユーザーエンティティ
 */
export interface User {
  /** ユーザーID */
  id: string
  /** ユーザー名 */
  name: string
  /** メールアドレス */
  email: string
  /** ユーザーロール */
  role: UserRole
}

/**
 * ユーザー作成リクエスト
 */
export interface CreateUserRequest {
  /** ユーザー名 */
  name: string
  /** メールアドレス */
  email: string
  /** ユーザーロール */
  role: UserRole
}

/**
 * ページネーション情報
 */
export interface Pagination {
  /** 現在のページ番号（1始まり） */
  page: number
  /** 1ページあたりの件数 */
  page_size: number
  /** 総件数 */
  total: number
  /** 総ページ数 */
  total_pages: number
}

/**
 * ユーザー一覧レスポンス
 */
export interface UsersResponse {
  /** ユーザーリスト */
  users: User[]
  /** ページネーション情報 */
  pagination: Pagination
}
