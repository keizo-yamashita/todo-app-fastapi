/**
 * 新規登録フォームのContainerコンポーネント
 */

'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { apiClient } from '@/lib/api-client'
import { ApiError } from '@/types/api'
import type { RegisterRequest } from '@/types/auth'
import { RegisterForm } from './register-form'

/**
 * 新規登録フォームのContainerコンポーネント
 */
export const RegisterFormContainer = () => {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [passwordConfirm, setPasswordConfirm] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    // パスワード確認チェック
    if (password !== passwordConfirm) {
      setError('パスワードが一致しません')
      return
    }

    // パスワードの長さチェック
    if (password.length < 8) {
      setError('パスワードは8文字以上で入力してください')
      return
    }

    setIsSubmitting(true)

    try {
      const request: RegisterRequest = {
        email,
        name,
        password,
      }

      await apiClient.post('/api/auth/register', request)

      // 登録成功後、ログインページへ遷移（成功フラグ付き）
      router.push('/login?registered=true')
    } catch (err) {
      console.error('Registration error:', err)
      if (err instanceof ApiError) {
        // APIエラーコードに基づいてユーザーフレンドリーなメッセージに変換
        switch (err.code) {
          case 'USER_EMAIL_ALREADY_EXISTS':
            setError('このメールアドレスは既に登録されています')
            break
          case 'INVALID_VALUE':
            // 詳細なエラーメッセージがあれば表示
            if (err.details && err.details.error) {
              const errorDetail = String(err.details.error)
              if (errorDetail.includes('email')) {
                setError('メールアドレスの形式が正しくありません')
              } else if (errorDetail.includes('name')) {
                setError('名前は1文字以上100文字以下で入力してください')
              } else if (errorDetail.includes('password')) {
                setError('パスワードが長すぎます。72文字以下で入力してください')
              } else {
                setError(`入力内容に誤りがあります: ${errorDetail}`)
              }
            } else {
              setError('入力内容に誤りがあります。もう一度確認してください')
            }
            break
          default:
            setError(
              `登録に失敗しました (エラーコード: ${err.code || 'UNKNOWN'})`
            )
        }
      } else if (err instanceof Error) {
        setError(err.message)
      } else {
        setError('登録に失敗しました')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <RegisterForm
      email={email}
      name={name}
      password={password}
      passwordConfirm={passwordConfirm}
      isSubmitting={isSubmitting}
      error={error}
      onEmailChange={setEmail}
      onNameChange={setName}
      onPasswordChange={setPassword}
      onPasswordConfirmChange={setPasswordConfirm}
      onSubmit={handleSubmit}
    />
  )
}
