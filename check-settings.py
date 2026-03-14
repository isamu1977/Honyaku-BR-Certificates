#!/usr/bin/env python3
"""
バックエンドとフロントエンドの設定が正しく揃っているか確認するスクリプト
"""
import os
import re
import sys

def check_backend_port():
    """バックエンドのポート設定を確認"""
    print("🔍 バックエンドのポート設定を確認中...")
    
    backend_main = "backend/main.py"
    if not os.path.exists(backend_main):
        print(f"  ❌ {backend_main} が見つかりません")
        return None
    
    with open(backend_main, "r") as f:
        content = f.read()
    
    # find_free_port 関数の存在を確認
    if "find_free_port" in content:
        print("  ✅ ポート自動選択関数 find_free_port() が実装されています")
    else:
        print("  ⚠️  ポート自動選択関数が見つかりません")
    
    return 8080  # デフォルトポート

def check_frontend_env():
    """フロントエンドの環境変数設定を確認"""
    print("\n🔍 フロントエンドの環境変数設定を確認中...")
    
    env_file = "front/.env"
    if not os.path.exists(env_file):
        print(f"  ❌ {env_file} が見つかりません")
        return None
    
    with open(env_file, "r") as f:
        content = f.read()
    
    # VITE_BACKEND_URL の確認
    match = re.search(r'VITE_BACKEND_URL=(http://[^\s]+)', content)
    if match:
        url = match.group(1)
        print(f"  ✅ VITE_BACKEND_URL が設定されています：{url}")
        return url
    else:
        print("  ❌ VITE_BACKEND_URL が見つかりません")
        return None

def check_frontend_code():
    """フロントエンドのコードで BACKEND_URL が使用されているか確認"""
    print("\n🔍 フロントエンドのコード設定を確認中...")
    
    files_to_check = [
        "front/src/routes/+page.svelte",
        "front/src/lib/stores/certificationStore.js"
    ]
    
    all_ok = True
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"  ❌ {file_path} が見つかりません")
            all_ok = False
            continue
        
        with open(file_path, "r") as f:
            content = f.read()
        
        # BACKEND_URL または import.meta.env.VITE_BACKEND_URL の使用を確認
        if "BACKEND_URL" in content or "VITE_BACKEND_URL" in content:
            print(f"  ✅ {file_path} - 環境変数を使用")
        elif "localhost:8080" in content or "localhost:8000" in content:
            print(f"  ⚠️  {file_path} - ハードコードされた URL が残っている可能性があります")
        else:
            print(f"  ℹ️  {file_path} - URL 設定なし")
    
    return all_ok

def check_port_conflict(port):
    """ポートの競合を確認"""
    print(f"\n🔍 ポート {port} の競合を確認中...")
    
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('localhost', port))
            print(f"  ✅ ポート {port} は利用可能です")
            return True
    except OSError:
        print(f"  ⚠️  ポート {port} は既に使用されています")
        return False

def main():
    print("=" * 60)
    print("🔧 Honyaku App 設定チェック")
    print("=" * 60)
    
    # プロジェクトルートを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    backend_port = check_backend_port()
    frontend_url = check_frontend_env()
    check_frontend_code()
    
    if backend_port:
        check_port_conflict(backend_port)
    
    print("\n" + "=" * 60)
    print("✅ 設定チェック完了")
    print("=" * 60)
    
    # 起動コマンドの表示
    print("\n📋 起動コマンド:")
    print("  # 個別起動:")
    print("  cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8080")
    print("  cd front && npm run dev")
    print("")
    print("  # または一括起動スクリプト:")
    print("  ./start-all.sh")

if __name__ == "__main__":
    main()
