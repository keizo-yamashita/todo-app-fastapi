import { expect, test } from '@playwright/test'

import {
  generateLongEmailUser,
  generateSpecialCharEmailUser,
  generateTestUser,
  testUsers,
} from '../fixtures/test-data'
import { LoginPage } from '../page-objects/login-page'
import { RegisterPage } from '../page-objects/register-page'

/**
 * 新規登録フローのE2Eテスト
 */
test.describe('新規登録フロー', () => {
  test.beforeEach(async ({ page }) => {
    const registerPage = new RegisterPage(page)
    await registerPage.goto()
  })

  test('正常系: 有効なユーザー情報で新規登録できる', async ({ page }) => {
    const registerPage = new RegisterPage(page)
    const loginPage = new LoginPage(page)
    const testUser = generateTestUser()

    // 新規登録を実行
    await registerPage.register(testUser)

    // ログインページにリダイレクトされることを確認
    await page.waitForURL('**/login*')
    await expect(page).toHaveURL(/\/login/)

    // 登録したユーザーでログインできることを確認
    await loginPage.login(testUser)
    await page.waitForURL('**/')
    await expect(page).toHaveURL(/\/$/)
  })

  test('正常系: 登録成功後に適切なメッセージが表示される', async ({ page }) => {
    const registerPage = new RegisterPage(page)
    const testUser = generateTestUser()

    // 新規登録を実行
    await registerPage.register(testUser)

    // ログインページにリダイレクトされることを確認
    await page.waitForURL('**/login**')
    await expect(page).toHaveURL(/\/login/)

    // 成功メッセージが表示されることを確認
    const successMessage = page.locator('div[class*="success"]')
    await expect(successMessage).toBeVisible()
    await expect(successMessage).toContainText('登録が完了しました')
  })

  test('異常系: 既に登録済みのメールアドレスではエラーが表示される', async ({
    page,
  }) => {
    const registerPage = new RegisterPage(page)
    const testUser = generateTestUser()

    // 1回目の登録（成功）
    await registerPage.register(testUser)
    await page.waitForURL('**/login*')

    // 2回目の登録を試みる（失敗を期待）
    await registerPage.goto()
    await registerPage.register(testUser)

    // エラーメッセージが表示されることを確認
    const errorMessage = await registerPage.expectErrorMessage(
      'このメールアドレスは既に登録されています'
    )
    await expect(errorMessage).toContainText('既に登録されています')

    // 登録ページに留まることを確認
    await expect(page).toHaveURL(/\/register/)
  })

  test('異常系: パスワードが一致しない場合はエラーが表示される', async ({
    page,
  }) => {
    const registerPage = new RegisterPage(page)
    const testUser = generateTestUser()

    // パスワードと確認用パスワードを異なる値で入力
    await registerPage.registerWithMismatchedPassword(
      testUser,
      'DifferentPassword123!'
    )

    // エラーメッセージが表示されることを確認
    const errorMessage =
      await registerPage.expectErrorMessage('パスワードが一致しません')
    await expect(errorMessage).toContainText('一致しません')

    // 登録ページに留まることを確認
    await expect(page).toHaveURL(/\/register/)
  })

  test('異常系: パスワードが短すぎる場合はHTML5バリデーションが動作する', async ({
    page,
  }) => {
    const registerPage = new RegisterPage(page)

    // 短すぎるパスワードを入力
    await registerPage.emailInput.fill(testUsers.shortPassword.email)
    await registerPage.nameInput.fill(testUsers.shortPassword.name)
    await registerPage.passwordInput.fill(testUsers.shortPassword.password)
    await registerPage.passwordConfirmInput.fill(
      testUsers.shortPassword.password
    )

    // 送信ボタンをクリック
    await registerPage.submitButton.click()

    // HTML5バリデーションにより、ページが遷移しないことを確認
    await expect(page).toHaveURL(/\/register/)

    // パスワード入力フィールドのバリデーション状態を確認
    const isValid = await registerPage.passwordInput.evaluate(
      (el: HTMLInputElement) => el.checkValidity()
    )
    expect(isValid).toBe(false)
  })

  test('異常系: 無効なメールアドレス形式ではHTML5バリデーションが動作する', async ({
    page,
  }) => {
    const registerPage = new RegisterPage(page)

    // 無効なメールアドレスを入力
    await registerPage.emailInput.fill(testUsers.invalidEmail.email)
    await registerPage.nameInput.fill(testUsers.invalidEmail.name)
    await registerPage.passwordInput.fill(testUsers.invalidEmail.password)
    await registerPage.passwordConfirmInput.fill(
      testUsers.invalidEmail.password
    )

    // 送信ボタンをクリック
    await registerPage.submitButton.click()

    // HTML5バリデーションにより、ページが遷移しないことを確認
    await expect(page).toHaveURL(/\/register/)

    // メールアドレス入力フィールドのバリデーション状態を確認
    const isValid = await registerPage.emailInput.evaluate(
      (el: HTMLInputElement) => el.checkValidity()
    )
    expect(isValid).toBe(false)
  })

  test('UI: ログインページへのリンクが機能する', async ({ page }) => {
    const registerPage = new RegisterPage(page)

    // ログインページへのリンクをクリック
    await registerPage.goToLogin()

    // ログインページに遷移することを確認
    await page.waitForURL('**/login*')
    await expect(page).toHaveURL(/\/login/)
  })

  test('異常系: メールアドレスが空の場合はHTML5バリデーションが動作する', async ({
    page,
  }) => {
    const registerPage = new RegisterPage(page)

    // メールアドレスを空にして送信
    await registerPage.nameInput.fill('Test User')
    await registerPage.passwordInput.fill('password123')
    await registerPage.passwordConfirmInput.fill('password123')
    await registerPage.submitButton.click()

    // ページが遷移しないことを確認
    await expect(page).toHaveURL(/\/register/)

    // バリデーション状態を確認
    const isValid = await registerPage.emailInput.evaluate(
      (el: HTMLInputElement) => el.checkValidity()
    )
    expect(isValid).toBe(false)
  })

  test('異常系: 名前が空の場合はHTML5バリデーションが動作する', async ({
    page,
  }) => {
    const registerPage = new RegisterPage(page)

    await registerPage.emailInput.fill('test@example.com')
    // 名前を空にして送信
    await registerPage.passwordInput.fill('password123')
    await registerPage.passwordConfirmInput.fill('password123')
    await registerPage.submitButton.click()

    await expect(page).toHaveURL(/\/register/)

    const isValid = await registerPage.nameInput.evaluate(
      (el: HTMLInputElement) => el.checkValidity()
    )
    expect(isValid).toBe(false)
  })

  test('異常系: パスワードが空の場合はHTML5バリデーションが動作する', async ({
    page,
  }) => {
    const registerPage = new RegisterPage(page)

    await registerPage.emailInput.fill('test@example.com')
    await registerPage.nameInput.fill('Test User')
    // パスワードを空にして送信
    await registerPage.passwordConfirmInput.fill('password123')
    await registerPage.submitButton.click()

    await expect(page).toHaveURL(/\/register/)

    const isValid = await registerPage.passwordInput.evaluate(
      (el: HTMLInputElement) => el.checkValidity()
    )
    expect(isValid).toBe(false)
  })

  test('UI: 送信中はボタンが無効化される', async ({ page }) => {
    const registerPage = new RegisterPage(page)
    const testUser = generateTestUser()

    await registerPage.emailInput.fill(testUser.email)
    await registerPage.nameInput.fill(testUser.name)
    await registerPage.passwordInput.fill(testUser.password)
    await registerPage.passwordConfirmInput.fill(testUser.password)

    // 送信ボタンをクリック
    const submitPromise = registerPage.submitButton.click()

    // 送信中はボタンが無効化されていることを確認
    await expect(registerPage.submitButton).toBeDisabled()
    await expect(registerPage.submitButton).toContainText('登録中')

    await submitPromise
  })

  test('エッジケース: 特殊文字を含むメールアドレスで登録できる', async ({
    page,
  }) => {
    const registerPage = new RegisterPage(page)
    const loginPage = new LoginPage(page)

    // 特殊文字を含むメールアドレスで登録
    const specialUser = generateSpecialCharEmailUser()

    await registerPage.register(specialUser)
    await page.waitForURL('**/login*')

    // 登録したユーザーでログインできることを確認
    await loginPage.login(specialUser)
    await page.waitForURL('**/')
    await expect(page).toHaveURL(/\/$/)
  })

  test('エッジケース: 長いメールアドレスで登録できる', async ({ page }) => {
    const registerPage = new RegisterPage(page)
    const loginPage = new LoginPage(page)

    // 長いメールアドレスで登録（ただしバックエンドの制限内）
    const longEmailUser = generateLongEmailUser()

    await registerPage.register(longEmailUser)
    await page.waitForURL('**/login*')

    // 登録したユーザーでログインできることを確認
    await loginPage.login(longEmailUser)
    await page.waitForURL('**/')
    await expect(page).toHaveURL(/\/$/)
  })
})
