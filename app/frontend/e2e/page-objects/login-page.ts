import { type Locator, type Page } from '@playwright/test'

import type { TestUser } from '../fixtures/test-data'

/**
 * ログインページのPage Object Model
 */
export class LoginPage {
  /** Playwrightのページオブジェクト */
  readonly page: Page

  /** メールアドレス入力フィールド */
  readonly emailInput: Locator

  /** パスワード入力フィールド */
  readonly passwordInput: Locator

  /** ログインボタン */
  readonly submitButton: Locator

  /** エラーメッセージ */
  readonly errorMessage: Locator

  /** 新規登録リンク */
  readonly registerLink: Locator

  /**
   * LoginPageを初期化する
   *
   * @param page Playwrightのページオブジェクト
   */
  constructor(page: Page) {
    this.page = page
    this.emailInput = page.locator('input[type="email"]#email')
    this.passwordInput = page.locator('input[type="password"]#password')
    this.submitButton = page.locator('button[type="submit"]')
    this.errorMessage = page.locator('div[class*="error"]')
    this.registerLink = page.locator('a', { hasText: '新規登録' })
  }

  /**
   * ログインページに遷移する
   */
  async goto() {
    await this.page.goto('/login')
  }

  /**
   * ユーザー情報を入力してログインする
   *
   * @param user ユーザー情報
   */
  async login(user: TestUser) {
    await this.emailInput.fill(user.email)
    await this.passwordInput.fill(user.password)
    await this.submitButton.click()
  }

  /**
   * メールアドレスとパスワードを個別に指定してログインする
   *
   * @param email メールアドレス
   * @param password パスワード
   */
  async loginWith(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
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
   * 新規登録ページへのリンクをクリックする
   */
  async goToRegister() {
    await this.registerLink.click()
  }
}
