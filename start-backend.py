#!/usr/bin/env python3
"""
バックエンドサーバー起動スクリプト
ポートが使用中の場合は自動的に別のポートを探す
"""
import os
import sys
import socket
import subprocess
import time

def find_free_port(start_port: int = 8080, max_attempts: int = 10) -> int:
    """
    空いているポートを自動的に見つける
    start_port から始めて、最大 max_attempts 回試行
    """
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('localhost', port))
                return port
        except OSError:
            continue  # ポートが使用中の場合は次に進む
    
    # すべてのポートが使用中の場合は 0 を返す（OS が自動割り当て）
    return 0

def main():
    # バックエンドディレクトリに移動
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(script_dir, "backend")
    os.chdir(backend_dir)
    
    # 仮想環境の activate
    venv_activate = os.path.join(backend_dir, "venv", "bin", "activate")
    if os.path.exists(venv_activate):
        # 仮想環境を有効化して uvicorn を起動
        cmd = f"source {venv_activate} && exec uvicorn main:app --reload --host 0.0.0.0 --port 8080"
    else:
        # 仮想環境がない場合は直接 uvicorn を起動
        cmd = "exec uvicorn main:app --reload --host 0.0.0.0 --port 8080"
    
    print(f"🚀 バックエンドサーバーを起動中...")
    print(f"📍 ディレクトリ：{backend_dir}")
    print(f"🔌 ポート：8080（自動フォールバック対応）")
    print(f"💡 停止するには Ctrl+C を押してください")
    print("-" * 50)
    
    # bash でコマンドを実行
    os.system(f"bash -c '{cmd}'")

if __name__ == "__main__":
    main()
