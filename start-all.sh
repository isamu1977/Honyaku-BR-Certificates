#!/bin/bash
# フロントエンド・バックエンド同時起動スクリプト

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONT_DIR="$SCRIPT_DIR/front"

echo "🚀 Honyaku App 起動スクリプト"
echo "================================"
echo ""

# バックエンドの起動
echo "📦 バックエンドを起動中..."
cd "$BACKEND_DIR"
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8080 &
BACKEND_PID=$!
echo "✅ バックエンド起動完了 (PID: $BACKEND_PID)"
echo ""

# フロントエンドの起動
echo "🎨 フロントエンドを起動中..."
cd "$FRONT_DIR"
npm run dev &
FRONT_PID=$!
echo "✅ フロントエンド起動完了 (PID: $FRONT_PID)"
echo ""

echo "================================"
echo "📍 バックエンド：http://localhost:8080"
echo "🎨 フロントエンド：http://localhost:5173"
echo ""
echo "⏹️  停止するには Ctrl+C を押してください"
echo ""

# 両方のプロセスを待機
wait
