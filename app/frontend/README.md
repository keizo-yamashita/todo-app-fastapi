# Todo App Frontend

Next.js 16 (App Router) を使用したTodoアプリケーションのフロントエンドです。

## 技術スタック

- **フレームワーク**: Next.js 16 (App Router)
- **言語**: TypeScript
- **スタイリング**: CSS Modules
- **バリデーション**: Zod
- **リンター**: ESLint
- **フォーマッター**: Prettier

## アーキテクチャ

このプロジェクトは **Container/Presentationパターン** を採用しています。

### Container/Presentationパターンの特徴

- **Presentation Components（`*.tsx`）**: UIの表示のみを担当する純粋な関数コンポーネント
- **Container Components（`*.container.tsx`）**: データ取得、状態管理、ビジネスロジックを担当

### ディレクトリ構造

```
src/
├── app/                          # Next.js App Router（ルーティング）
│   ├── layout.tsx               # ルートレイアウト
│   ├── page.tsx                 # ホームページ
│   └── globals.css              # グローバルスタイル
├── features/                     # 機能ディレクトリ（APIエンドポイントと対応）
│   └── users/
│       ├── components/           # ユーザー機能固有コンポーネント
│       │   ├── user-list/
│       │   │   ├── user-list.tsx              # Presentation
│       │   │   ├── user-list.module.css
│       │   │   └── index.tsx
│       │   ├── user-form/
│       │   │   ├── user-form.tsx              # Presentation
│       │   │   ├── user-form.container.tsx    # Container
│       │   │   ├── user-form.module.css
│       │   │   └── index.tsx
│       │   └── users-page/
│       │       ├── users-page.tsx             # Presentation
│       │       ├── users-page.container.tsx   # Container
│       │       ├── users-page.module.css
│       │       └── index.tsx
│       └── index.ts
├── components/                   # 共通（汎用）コンポーネント
│   ├── error-message/
│   │   ├── error-message.tsx
│   │   ├── error-message.module.css
│   │   └── index.tsx
│   └── pagination/
│       ├── pagination.tsx
│       ├── pagination.module.css
│       └── index.tsx
├── lib/                         # ユーティリティ関数とAPIクライアント
│   ├── api-client.ts           # バックエンドAPIクライアント
│   └── utils.ts                # ユーティリティ関数
└── types/                       # TypeScript型定義
    ├── user.ts                 # ユーザー関連型
    └── api.ts                  # API関連型
```

## セットアップ

### 依存関係のインストール

```bash
npm install
```

### 環境変数の設定

`.env.local` ファイルを作成し、以下の環境変数を設定してください：

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 開発サーバーの起動

```bash
npm run dev
```

ブラウザで [http://localhost:3000](http://localhost:3000) を開いてください。

## スクリプト

### 開発サーバー

- `npm run dev` - 開発サーバーを起動
- `npm run build` - 本番用ビルドを作成
- `npm start` - 本番サーバーを起動

### 品質保証

- `npm run format:check` - Prettierのフォーマットチェック
- `npm run format` - Prettierでコードを整形
- `npm run lint` - ESLintでコードをチェック
- `npm run type-check` - TypeScriptの型チェック

## 開発ガイドライン

### コンポーネント作成ルール

#### Presentation Components

- propsの型を `interface` で明確に定義
- 純粋関数として実装（同じpropsなら同じ結果）
- 状態管理・副作用・API通信は一切行わない
- UIの表示のみを担当

#### Container Components

- データ取得、状態管理、イベントハンドリングを担当
- Presentationコンポーネントにpropsを渡す
- DOM構造やスタイリングは扱わない（Presentationに委譲）

### 共通化の基準

- **`components/`**: 汎用で再利用できるコンポーネントのみ
- **`features/**/components/`\*\*: 画面/ドメインに依存するUI

## 品質保証

### コード変更時の基本フロー

コード変更後は以下の順序で実行し、すべてパスすることを確認してください：

```bash
# 1. フォーマットチェック
npm run format:check

# 2. フォーマット実行（差分がある場合）
npm run format

# 3. リンターチェック
npm run lint

# 4. 型チェック
npm run type-check
```

### コミット前の必須チェック

**重要**: プルリクエストを作成する前に、必ずすべてのチェックがパスすることを確認してください。

### チェック内容

- **フォーマット**: Prettierを実行し、差分が0であること
- **リンター**: ESLintを実行し、エラー・警告が0であること
- **型チェック**: TypeScriptコンパイラを実行し、型エラーが0であること

詳細なルールについては、`.cursor/rules/coding-rules/02-frontend/03-typescript-quality-check.mdc` を参照してください。
