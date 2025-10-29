/**
 * E2Eテスト用のテストデータ
 */

/**
 * ユーザー情報の型定義
 */
export interface TestUser {
  /** メールアドレス */
  email: string
  /** ユーザー名 */
  name: string
  /** パスワード */
  password: string
}

/**
 * テスト用ユーザーデータ
 */
export const testUsers = {
  /** 新規登録用の有効なユーザー */
  validUser: {
    email: `test-${Date.now()}@example.com`,
    name: 'テストユーザー',
    password: 'TestPassword123!',
  } as TestUser,

  /** 既存ユーザー（事前に登録済み） */
  existingUser: {
    email: 'existing@example.com',
    name: '既存ユーザー',
    password: 'ExistingPassword123!',
  } as TestUser,

  /** 無効なメールアドレス */
  invalidEmail: {
    email: 'invalid-email',
    name: 'テストユーザー',
    password: 'TestPassword123!',
  } as TestUser,

  /** パスワードが短すぎる */
  shortPassword: {
    email: `test-${Date.now()}@example.com`,
    name: 'テストユーザー',
    password: 'short',
  } as TestUser,

  /** 間違ったパスワード */
  wrongPassword: {
    email: 'existing@example.com',
    name: '既存ユーザー',
    password: 'WrongPassword123!',
  } as TestUser,
}

/**
 * 新しいテストユーザーを生成する
 *
 * @returns 新しいテストユーザー
 */
export function generateTestUser(): TestUser {
  return {
    email: `test-${Date.now()}-${Math.random().toString(36).substring(7)}@example.com`,
    name: `テストユーザー${Math.random().toString(36).substring(7)}`,
    password: 'TestPassword123!',
  }
}

/**
 * 特殊文字を含むメールアドレスのテストユーザーを生成する
 *
 * @returns 特殊文字を含むメールアドレスのテストユーザー
 */
export function generateSpecialCharEmailUser(): TestUser {
  const uniqueId = `${Date.now()}-${Math.random().toString(36).substring(7)}`
  return {
    email: `test+tag-${uniqueId}@example.com`,
    name: 'Special User',
    password: 'TestPassword123!',
  }
}

/**
 * 長いメールアドレスのテストユーザーを生成する
 *
 * @returns 長いメールアドレスのテストユーザー
 */
export function generateLongEmailUser(): TestUser {
  const uniqueId = `${Date.now()}-${Math.random().toString(36).substring(7)}`
  return {
    email: `verylongemailaddress-${uniqueId}-1234567890@example.com`,
    name: 'Long Email User',
    password: 'TestPassword123!',
  }
}
