import { defineConfig, devices } from '@playwright/test'

/**
 * Playwright設定
 *
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  // テストディレクトリ
  testDir: './e2e',

  // テストの最大実行時間
  timeout: 30 * 1000,

  // 各テストの前に実行する期待値の設定
  expect: {
    timeout: 5000,
  },

  // 失敗したテストのみリトライ
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,

  // CI環境では並列実行数を制限
  workers: process.env.CI ? 1 : undefined,

  // レポート設定
  reporter: [['html', { outputFolder: 'playwright-report' }], ['list']],

  // 共通設定
  use: {
    // ベースURL
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000',

    // スクリーンショット設定
    screenshot: 'only-on-failure',

    // ビデオ録画設定
    video: 'retain-on-failure',

    // トレース設定
    trace: 'retain-on-failure',

    // ナビゲーション待機設定
    actionTimeout: 10 * 1000,
    navigationTimeout: 30 * 1000,
  },

  // テスト対象ブラウザ
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    // Firefox と Webkit は必要に応じてコメントアウトを解除
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    // モバイルブラウザのテスト
    // {
    //   name: 'Mobile Chrome',
    //   use: { ...devices['Pixel 5'] },
    // },

    // {
    //   name: 'Mobile Safari',
    //   use: { ...devices['iPhone 12'] },
    // },
  ],

  // 開発サーバーの起動設定（必要に応じて有効化）
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
})
