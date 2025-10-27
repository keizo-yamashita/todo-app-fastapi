'use client'

import { useState, FormEvent } from 'react'
import { CreateUserRequest } from '@/types/user'
import { UserForm } from './user-form'

/**
 * ユーザーフォームコンテナのプロパティ
 */
interface UserFormContainerProps {
  /** フォーム送信時のコールバック */
  onSubmit: (data: CreateUserRequest) => Promise<void>
  /** 送信中かどうか */
  isSubmitting: boolean
}

/**
 * ユーザーフォーム Containerコンポーネント
 *
 * フォームの状態管理とビジネスロジックを担当する
 *
 * @param props コンポーネントのプロパティ
 * @returns ユーザーフォームコンテナコンポーネント
 */
export function UserFormContainer({
  onSubmit,
  isSubmitting,
}: UserFormContainerProps) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [role, setRole] = useState<'user' | 'admin'>('user')

  /**
   * フォーム送信ハンドラ
   *
   * @param e フォームイベント
   */
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    await onSubmit({ name, email, role })

    // 送信成功後、フォームをリセット
    setName('')
    setEmail('')
    setRole('user')
  }

  return (
    <UserForm
      name={name}
      onNameChange={setName}
      email={email}
      onEmailChange={setEmail}
      role={role}
      onRoleChange={setRole}
      onSubmit={handleSubmit}
      isSubmitting={isSubmitting}
    />
  )
}
