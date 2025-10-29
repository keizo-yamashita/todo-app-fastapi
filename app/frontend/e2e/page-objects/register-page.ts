import { type Locator, type Page } from '@playwright/test'

import type { TestUser } from '../fixtures/test-data'

/**
 * 新規登録ページのPage Object Model
 */
export class RegisterPage {
  /** Playwrightのページオブジェクト */
  readonly page: Page

  /** メールアドレス入力フィールド */
  readonly emailInput: Locator

  /** ユーザー名入力フィールド */
  readonly nameInput: Locator

  /** パスワード入力フィールド */
  readonly passwordInput: Locator

  /** パスワード確認入力フィールド */
  readonly passwordConfirmInput: Locator

  /** 登録ボタン */
  readonly submitButton: Locator

  /** エラーメッセージ */
  readonly errorMessage: Locator

  /** ログインリンク */
  readonly loginLink: Locator

  /**
   * RegisterPageを初期化する
   *
   * @param page Playwrightのページオブジェクト
   */
  constructor(page: Page) {
    this.page = page
    this.emailInput = page.locator('input[type="email"]#email')
    this.nameInput = page.locator('input[type="text"]#name')
    this.passwordInput = page.locator('input[type="password"]#password')
    this.passwordConfirmInput = page.locator(
      'input[type="password"]#passwordConfirm'
    )
    this.submitButton = page.locator('button[type="submit"]')
    this.errorMessage = page.locator('div[class*="error"]')
    this.loginLink = page.locator('a', { hasText: 'ログイン' })
  }

  /**
   * 登録ページに遷移する
   */
  async goto() {
    await this.page.goto('/register')
  }

  /**
   * ユーザー情報を入力して登録する
   *
   * @param user ユーザー情報
   */
  async register(user: TestUser) {
    await this.emailInput.fill(user.email)
    await this.nameInput.fill(user.name)
    await this.passwordInput.fill(user.password)
    await this.passwordConfirmInput.fill(user.password)
    await this.submitButton.click()
  }

  /**
   * パスワード不一致で登録を試みる
   *
   * @param user ユーザー情報
   * @param confirmPassword 確認用パスワード
   */
  async registerWithMismatchedPassword(
    user: TestUser,
    confirmPassword: string
  ) {
    await this.emailInput.fill(user.email)
    await this.nameInput.fill(user.name)
    await this.passwordInput.fill(user.password)
    await this.passwordConfirmInput.fill(confirmPassword)
    await this.submitButton.click()
  }

  /**
   * エラーメッセージが表示されているか確認する
   *
   * @param _expectedMessage 期待されるエラーメッセージ（テストコードで検証）
   */
  async expectErrorMessage(_expectedMessage: string) {
    await this.errorMessage.waitFor({ state: 'visible' })
    return this.errorMessage
  }

  /**
   * ログインページへのリンクをクリックする
   */
  async goToLogin() {
    await this.loginLink.click()
  }
}
