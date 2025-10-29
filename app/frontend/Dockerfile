# ベースイメージ
FROM node:22-alpine AS base

# 依存関係をインストールするステージ
FROM base AS deps
WORKDIR /app

# 依存関係ファイルをコピー
COPY package.json package-lock.json* ./

# 依存関係をインストール
RUN npm ci

# アプリケーションをビルドするステージ
FROM base AS builder
WORKDIR /app

# 依存関係をコピー
COPY --from=deps /app/node_modules ./node_modules

# ソースコードをコピー
COPY . .

# 環境変数を設定（ビルド時）
ENV NEXT_TELEMETRY_DISABLED=1

# アプリケーションをビルド
RUN npm run build

# 本番環境用のステージ
FROM base AS runner
WORKDIR /app

# 環境変数を設定
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# 非rootユーザーを作成
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# 必要なファイルをコピー
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# 非rootユーザーに切り替え
USER nextjs

# ポートを公開
EXPOSE 3000

# 環境変数を設定
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# アプリケーションを起動
CMD ["node", "server.js"]

