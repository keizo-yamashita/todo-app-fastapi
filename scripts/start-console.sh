#!/bin/bash

# Next.js (Console) を起動するスクリプト

echo "🚀 Starting Next.js Console..."

cd /app/packages/console

# 依存関係がインストールされていない場合はインストール
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    pnpm install
fi

# 開発サーバーを起動
echo "🌐 Starting development server on http://localhost:3000"
pnpm dev





