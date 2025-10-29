'use client'

import { Pagination as PaginationType } from '@/types/user'
import styles from './pagination.module.css'

/**
 * ページネーションコンポーネントのプロパティ
 */
interface PaginationProps {
  /** ページネーション情報 */
  pagination: PaginationType
  /** ページ変更時のコールバック */
  onPageChange: (page: number) => void
}

/**
 * ページネーション Presentationコンポーネント
 *
 * ページ切り替えUIを提供する汎用コンポーネント（純粋な表示のみ）
 *
 * @param props コンポーネントのプロパティ
 * @returns ページネーションコンポーネント
 */
export function Pagination({ pagination, onPageChange }: PaginationProps) {
  const { page, total_pages } = pagination

  // ページ数が1以下の場合は表示しない
  if (total_pages <= 1) {
    return null
  }

  /**
   * 表示するページ番号の配列を生成する
   *
   * @returns ページ番号の配列
   */
  const getPageNumbers = (): (number | string)[] => {
    const pages: (number | string)[] = []
    const maxVisible = 7 // 最大表示ページ数

    if (total_pages <= maxVisible) {
      // 全ページを表示
      for (let i = 1; i <= total_pages; i++) {
        pages.push(i)
      }
    } else {
      // 省略表示
      if (page <= 4) {
        // 先頭付近
        for (let i = 1; i <= 5; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(total_pages)
      } else if (page >= total_pages - 3) {
        // 末尾付近
        pages.push(1)
        pages.push('...')
        for (let i = total_pages - 4; i <= total_pages; i++) {
          pages.push(i)
        }
      } else {
        // 中間
        pages.push(1)
        pages.push('...')
        for (let i = page - 1; i <= page + 1; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(total_pages)
      }
    }

    return pages
  }

  return (
    <nav className={styles.container} aria-label="ページネーション">
      <button
        className={styles.button}
        onClick={() => onPageChange(page - 1)}
        disabled={page === 1}
        aria-label="前のページ"
      >
        ‹ 前へ
      </button>

      {getPageNumbers().map((pageNum, index) =>
        typeof pageNum === 'number' ? (
          <button
            key={pageNum}
            className={`${styles.button} ${pageNum === page ? styles.active : ''}`}
            onClick={() => onPageChange(pageNum)}
            aria-label={`ページ ${pageNum}`}
            aria-current={pageNum === page ? 'page' : undefined}
          >
            {pageNum}
          </button>
        ) : (
          <span key={`ellipsis-${index}`} className={styles.ellipsis}>
            {pageNum}
          </span>
        )
      )}

      <button
        className={styles.button}
        onClick={() => onPageChange(page + 1)}
        disabled={page === total_pages}
        aria-label="次のページ"
      >
        次へ ›
      </button>
    </nav>
  )
}
