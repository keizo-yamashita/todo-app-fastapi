import type { Metadata } from 'next'
import './globals.css'

/**
 * メタデータ
 */
export const metadata: Metadata = {
  title: 'Todo App - ユーザー管理',
  description: 'Next.js 16で構築されたユーザー管理アプリケーション',
}

/**
 * ルートレイアウトのプロパティ
 */
interface RootLayoutProps {
  /** 子要素 */
  children: React.ReactNode
}

/**
 * ルートレイアウトコンポーネント
 *
 * アプリケーション全体のレイアウトを提供する
 *
 * @param props コンポーネントのプロパティ
 * @returns ルートレイアウトコンポーネント
 */
export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  )
}
