#!/bin/bash

# FastAPI と Next.js を同時に起動するスクリプト

echo "🚀 Starting Full Stack Development Environment..."

# バックグラウンドでFastAPIを起動
echo "📡 Starting FastAPI in background..."
cd /app/packages/core-api
piccolo migrations forwards core_api
nohup uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/fastapi.log 2>&1 &
FASTAPI_PID=$!

# Next.jsを起動
echo "🌐 Starting Next.js..."
cd /app/packages/console
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    pnpm install
fi

echo ""
echo "✅ Services starting:"
echo "   📡 FastAPI: http://localhost:8000 (PID: $FASTAPI_PID)"
echo "   🌐 Next.js: http://localhost:3000"
echo ""
echo "💡 To stop FastAPI: kill $FASTAPI_PID"
echo "💡 To view FastAPI logs: tail -f /tmp/fastapi.log"
echo ""

pnpm dev





