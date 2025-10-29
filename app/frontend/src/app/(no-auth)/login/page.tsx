/**
 * ログインページ
 */

import type { Metadata } from 'next'

import { LoginForm } from '@/features/auth'

/**
 * ページメタデータ
 */
export const metadata: Metadata = {
  title: 'ログイン | Todo App',
  description: 'アカウントにログイン',
}

/**
 * ログインページコンポーネント
 */
export default function LoginPage() {
  return <LoginForm />
}
