/**
 * ログインフォームのContainerコンポーネント
 */

'use client'

import { useRouter, useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { apiClient } from '@/lib/api-client'
import { ApiError } from '@/types/api'
import type { LoginRequest, LoginResponse } from '@/types/auth'
import { LoginForm } from './login-form'

/**
 * ログインフォームのContainerコンポーネント
 */
export const LoginFormContainer = () => {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  // URLパラメータから登録成功フラグを確認
  useEffect(() => {
    if (searchParams.get('registered') === 'true') {
      setSuccessMessage('登録が完了しました。ログインしてください。')
    }
  }, [searchParams])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
      const request: LoginRequest = {
        email,
        password,
      }

      const response = await apiClient.post<LoginResponse>(
        '/api/auth/login',
        request
      )

      // JWTトークンをlocalStorageに保存
      localStorage.setItem('access_token', response.access_token)

      // ログイン成功後、ホームページへ遷移
      router.push('/')
    } catch (err) {
      console.error('Login error:', err)
      if (err instanceof ApiError) {
        // APIエラーコードに基づいてユーザーフレンドリーなメッセージに変換
        switch (err.code) {
          case 'INVALID_CREDENTIALS':
            setError('メールアドレスまたはパスワードが正しくありません')
            break
          case 'INVALID_VALUE':
            setError('入力内容に誤りがあります')
            break
          case 'CREDENTIAL_NOT_FOUND':
          case 'USER_NOT_FOUND':
            setError('メールアドレスまたはパスワードが正しくありません')
            break
          default:
            setError(err.message || 'ログインに失敗しました')
        }
      } else if (err instanceof Error) {
        setError(err.message)
      } else {
        setError('ログインに失敗しました')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <LoginForm
      email={email}
      password={password}
      isSubmitting={isSubmitting}
      error={error}
      successMessage={successMessage}
      onEmailChange={setEmail}
      onPasswordChange={setPassword}
      onSubmit={handleSubmit}
    />
  )
}
