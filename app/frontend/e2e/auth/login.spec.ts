import { expect, test } from '@playwright/test'

import { generateTestUser, testUsers } from '../fixtures/test-data'
import { DashboardPage } from '../page-objects/dashboard-page'
import { LoginPage } from '../page-objects/login-page'
import { RegisterPage } from '../page-objects/register-page'

/**
 * ログインフローのE2Eテスト
 */
test.describe('ログインフロー', () => {
  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page)
    await loginPage.goto()
  })

  test('正常系: 有効な認証情報でログインできる', async ({ page }) => {
    const loginPage = new LoginPage(page)
    const dashboardPage = new DashboardPage(page)

    // 事前に新規ユーザーを登録
    const testUser = generateTestUser()
    const registerPage = new RegisterPage(page)
    await registerPage.goto()
    await registerPage.register(testUser)

    // ログインページに遷移
    await page.waitForURL('**/login*')

    // 登録したユーザーでログイン
    await loginPage.login(testUser)

    // ダッシュボードページにリダイレクトされることを確認
    await page.waitForURL('**/')
    await expect(page).toHaveURL(/\/$/)

    // ログイン状態の確認
    await dashboardPage.expectLoggedIn()
    await expect(dashboardPage.logoutButton).toBeVisible()
    await expect(dashboardPage.successMessage).toBeVisible()
  })

  test('異常系: 間違ったパスワードではエラーが表示される', async ({ page }) => {
    const loginPage = new LoginPage(page)

    // 間違ったパスワードでログインを試みる
    await loginPage.login(testUsers.wrongPassword)

    // エラーメッセージが表示されることを確認
    const errorMessage = await loginPage.expectErrorMessage(
      'メールアドレスまたはパスワードが正しくありません'
    )
    await expect(errorMessage).toContainText('正しくありません')

    // ログインページに留まることを確認
    await expect(page).toHaveURL(/\/login/)
  })

  test('異常系: 存在しないユーザーではエラーが表示される', async ({ page }) => {
    const loginPage = new LoginPage(page)
    const nonExistentUser = generateTestUser()

    // 存在しないユーザーでログインを試みる
    await loginPage.login(nonExistentUser)

    // エラーメッセージが表示されることを確認
    const errorMessage = await loginPage.expectErrorMessage(
      'メールアドレスまたはパスワードが正しくありません'
    )
    await expect(errorMessage).toContainText('正しくありません')

    // ログインページに留まることを確認
    await expect(page).toHaveURL(/\/login/)
  })

  test('異常系: 無効なメールアドレス形式ではHTML5バリデーションが動作する', async ({
    page,
  }) => {
    const loginPage = new LoginPage(page)

    // 無効なメールアドレスを入力
    await loginPage.emailInput.fill('invalid-email')
    await loginPage.passwordInput.fill('SomePassword123!')

    // 送信ボタンをクリック
    await loginPage.submitButton.click()

    // HTML5バリデーションにより、ページが遷移しないことを確認
    await expect(page).toHaveURL(/\/login/)

    // メールアドレス入力フィールドのバリデーション状態を確認
    const isValid = await loginPage.emailInput.evaluate(
      (el: HTMLInputElement) => el.checkValidity()
    )
    expect(isValid).toBe(false)
  })

  test('UI: 新規登録ページへのリンクが機能する', async ({ page }) => {
    const loginPage = new LoginPage(page)

    // 新規登録ページへのリンクをクリック
    await loginPage.goToRegister()

    // 新規登録ページに遷移することを確認
    await page.waitForURL('**/register')
    await expect(page).toHaveURL(/\/register/)
  })

  test('セッション: ログイン後にログアウトできる', async ({ page }) => {
    const loginPage = new LoginPage(page)
    const dashboardPage = new DashboardPage(page)

    // 事前に新規ユーザーを登録してログイン
    const testUser = generateTestUser()
    const registerPage = new RegisterPage(page)
    await registerPage.goto()
    await registerPage.register(testUser)
    await page.waitForURL('**/login*')
    await loginPage.login(testUser)
    await page.waitForURL('**/')

    // ログアウトボタンをクリック
    await dashboardPage.logout()

    // ログインページにリダイレクトされることを確認
    await page.waitForURL('**/login*')
    await expect(page).toHaveURL(/\/login/)
  })

  test('セッション: ログイン後にトークンが保存される', async ({ page }) => {
    const loginPage = new LoginPage(page)

    // 事前に新規ユーザーを登録
    const testUser = generateTestUser()
    const registerPage = new RegisterPage(page)
    await registerPage.goto()
    await registerPage.register(testUser)
    await page.waitForURL('**/login*')

    // ログイン
    await loginPage.login(testUser)
    await page.waitForURL('**/')

    // localStorageにトークンが保存されていることを確認
    const token = await page.evaluate(() =>
      localStorage.getItem('access_token')
    )
    expect(token).toBeTruthy()
    expect(typeof token).toBe('string')
  })

  test('セッション: ログアウト後にトークンが削除される', async ({ page }) => {
    const loginPage = new LoginPage(page)
    const dashboardPage = new DashboardPage(page)

    // 事前に新規ユーザーを登録してログイン
    const testUser = generateTestUser()
    const registerPage = new RegisterPage(page)
    await registerPage.goto()
    await registerPage.register(testUser)
    await page.waitForURL('**/login*')
    await loginPage.login(testUser)
    await page.waitForURL('**/')

    // ログアウト
    await dashboardPage.logout()
    await page.waitForURL('**/login*')

    // localStorageからトークンが削除されていることを確認
    const token = await page.evaluate(() =>
      localStorage.getItem('access_token')
    )
    expect(token).toBeNull()
  })

  test('認証: 未ログイン状態でダッシュボードにアクセスするとログインページにリダイレクトされる', async ({
    page,
  }) => {
    const dashboardPage = new DashboardPage(page)

    // ダッシュボードに直接アクセス
    await dashboardPage.goto()

    // ログインページにリダイレクトされることを確認
    await page.waitForURL('**/login*')
    await expect(page).toHaveURL(/\/login/)
  })

  test('異常系: メールアドレスが空の場合はHTML5バリデーションが動作する', async ({
    page,
  }) => {
    const loginPage = new LoginPage(page)

    // メールアドレスを空にして送信
    await loginPage.passwordInput.fill('password123')
    await loginPage.submitButton.click()

    await expect(page).toHaveURL(/\/login/)

    const isValid = await loginPage.emailInput.evaluate(
      (el: HTMLInputElement) => el.checkValidity()
    )
    expect(isValid).toBe(false)
  })

  test('異常系: パスワードが空の場合はHTML5バリデーションが動作する', async ({
    page,
  }) => {
    const loginPage = new LoginPage(page)

    await loginPage.emailInput.fill('test@example.com')
    // パスワードを空にして送信
    await loginPage.submitButton.click()

    await expect(page).toHaveURL(/\/login/)

    const isValid = await loginPage.passwordInput.evaluate(
      (el: HTMLInputElement) => el.checkValidity()
    )
    expect(isValid).toBe(false)
  })

  test('UI: 送信中はボタンが無効化される', async ({ page }) => {
    const loginPage = new LoginPage(page)
    const testUser = generateTestUser()

    // 事前に新規ユーザーを登録
    const registerPage = new RegisterPage(page)
    await registerPage.goto()
    await registerPage.register(testUser)
    await page.waitForURL('**/login*')

    // ログインフォームに入力
    await loginPage.emailInput.fill(testUser.email)
    await loginPage.passwordInput.fill(testUser.password)

    // 送信ボタンをクリック
    const submitPromise = loginPage.submitButton.click()

    // 送信中はボタンが無効化されていることを確認
    await expect(loginPage.submitButton).toBeDisabled()
    await expect(loginPage.submitButton).toContainText('ログイン中')

    await submitPromise
  })
})
