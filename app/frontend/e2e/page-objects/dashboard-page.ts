import { type Locator, type Page } from '@playwright/test'

/**
 * ダッシュボードページのPage Object Model
 */
export class DashboardPage {
  /** Playwrightのページオブジェクト */
  readonly page: Page

  /** ページタイトル */
  readonly pageTitle: Locator

  /** ダッシュボード見出し */
  readonly dashboardHeading: Locator

  /** ログアウトボタン */
  readonly logoutButton: Locator

  /** 成功メッセージ */
  readonly successMessage: Locator

  /**
   * DashboardPageを初期化する
   *
   * @param page Playwrightのページオブジェクト
   */
  constructor(page: Page) {
    this.page = page
    this.pageTitle = page.locator('h1').first()
    this.dashboardHeading = page.locator('h2', { hasText: 'ダッシュボード' })
    this.logoutButton = page.locator('button', { hasText: 'ログアウト' })
    this.successMessage = page.locator('p', {
      hasText: 'ログインに成功しました',
    })
  }

  /**
   * ダッシュボードページに遷移する
   */
  async goto() {
    await this.page.goto('/')
  }

  /**
   * ログアウトする
   */
  async logout() {
    await this.logoutButton.click()
  }

  /**
   * ログイン状態であることを確認する
   */
  async expectLoggedIn() {
    await this.dashboardHeading.waitFor({ state: 'visible' })
    await this.logoutButton.waitFor({ state: 'visible' })
  }
}
