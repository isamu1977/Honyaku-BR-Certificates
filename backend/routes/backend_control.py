from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import os
import signal
import psutil

router = APIRouter()

# グローバル変数でプロセス管理
backend_process = None
backend_pid = None

class BackendAction(BaseModel):
    action: str  # "start" or "stop"

@router.post("/api/start-backend")
async def toggle_backend(data: BackendAction):
    global backend_process, backend_pid
    
    try:
        if data.action == "start":
            # 既に稼働中の場合はエラー
            if backend_process is not None and backend_process.poll() is None:
                return {"success": True, "message": "Backend is already running"}
            
            # バックエンドディレクトリを取得
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            backend_dir = os.path.join(script_dir, "backend")
            venv_python = os.path.join(backend_dir, "venv", "bin", "python")
            main_py = os.path.join(backend_dir, "main.py")
            
            # uvicorn を起動
            if os.path.exists(venv_python):
                backend_process = subprocess.Popen(
                    [venv_python, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"],
                    cwd=backend_dir,
                    start_new_session=True
                )
                backend_pid = backend_process.pid
            else:
                # 仮想環境がない場合はシステム Python を使用
                backend_process = subprocess.Popen(
                    ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"],
                    cwd=backend_dir,
                    start_new_session=True
                )
                backend_pid = backend_process.pid
            
            return {"success": True, "message": f"Backend started on port 8080 (PID: {backend_pid})"}
            
        elif data.action == "stop":
            if backend_process is None:
                # プロセス情報がない場合は PID で探す
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        if 'uvicorn' in cmdline and 'main:app' in cmdline and '8080' in cmdline:
                            proc.terminate()
                            return {"success": True, "message": f"Backend stopped (PID: {proc.info['pid']})"}
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                return {"success": False, "error": "No running backend process found"}
            
            # プロセスを停止
            try:
                os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
                pid = backend_process.pid
                backend_process = None
                backend_pid = None
                return {"success": True, "message": f"Backend stopped (PID: {pid})"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Use 'start' or 'stop'")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/backend-status")
async def backend_status():
    """バックエンドの稼働状況を確認"""
    global backend_process, backend_pid
    
    # プロセスが稼働中かチェック
    if backend_process is not None and backend_process.poll() is None:
        return {"running": True, "pid": backend_pid}
    
    # PID でプロセスを探す
    if backend_pid:
        try:
            proc = psutil.Process(backend_pid)
            if proc.is_running():
                return {"running": True, "pid": backend_pid}
        except psutil.NoSuchProcess:
            pass
    
    # 別の方法で uvicorn プロセスを探す
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if 'uvicorn' in cmdline and 'main:app' in cmdline and '8080' in cmdline:
                return {"running": True, "pid": proc.info['pid']}
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return {"running": False}
