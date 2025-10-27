/**
 * 新規登録ページ
 */

import type { Metadata } from 'next'

import { RegisterForm } from '@/features/auth'

/**
 * ページメタデータ
 */
export const metadata: Metadata = {
  title: '新規登録 | Todo App',
  description: '新しいアカウントを作成',
}

/**
 * 新規登録ページコンポーネント
 */
export default function RegisterPage() {
  return <RegisterForm />
}
