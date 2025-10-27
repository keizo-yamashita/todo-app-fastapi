/**
 * ホームページ
 */

'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

import styles from './page.module.css'

/**
 * ホームページコンポーネント
 *
 * ログイン済みユーザーにはダッシュボードを表示し、
 * 未ログインユーザーはログインページにリダイレクトする。
 *
 * @returns ホームページコンポーネント
 */
export default function Home() {
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // ログイン状態を確認
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
    } else {
      setIsAuthenticated(true)
      setIsLoading(false)
    }
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    router.push('/login')
  }

  if (isLoading) {
    return <div className={styles.container}>Loading...</div>
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Todo App</h1>
        <button onClick={handleLogout} className={styles.logoutButton}>
          ログアウト
        </button>
      </div>
      <main className={styles.main}>
        <h2>ダッシュボード</h2>
        <p>ログインに成功しました！</p>
        <div className={styles.info}>
          <p>この画面は認証済みユーザーのみが閲覧できます。</p>
          <p>今後、TODOリスト機能を追加していきます。</p>
        </div>
      </main>
    </div>
  )
}
