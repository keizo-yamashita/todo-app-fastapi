#!/bin/bash

# FastAPI (core-api) を起動するスクリプト

echo "🚀 Starting FastAPI Core API..."

cd /app/packages/core-api

# マイグレーションを実行
echo "📊 Running database migrations..."
piccolo migrations forwards core_api

# 開発サーバーを起動
echo "🌐 Starting development server on http://localhost:8000"
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload





