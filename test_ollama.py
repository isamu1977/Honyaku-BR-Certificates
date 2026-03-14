"""
Ollama 接続テストスクリプト
"""
import requests
import base64
from io import BytesIO
from PIL import Image

# 1. Ollama サーバーの死活確認
print("=== Ollama サーバー確認 ===")
try:
    response = requests.get("http://localhost:11434/api/tags")
    if response.status_code == 200:
        print("✓ Ollama サーバーは稼働中")
        models = response.json().get("models", [])
        print(f"  利用可能なモデル数：{len(models)}")
        for m in models:
            print(f"    - {m['name']}")
    else:
        print(f"✗ Ollama サーバー応答異常：{response.status_code}")
except Exception as e:
    print(f"✗ Ollama サーバー接続エラー：{e}")

# 2. チャット API テスト（テキストのみ）
print("\n=== チャット API テスト ===")
try:
    payload = {
        "model": "qwen3.5:4b",
        "messages": [{"role": "user", "content": "Hello, test message"}],
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=60)
    if response.status_code == 200:
        data = response.json()
        content = data.get("message", {}).get("content", "")
        thinking = data.get("message", {}).get("thinking", "")
        print(f"✓ レスポンス成功")
        print(f"  コンテンツ（先頭 100 文字）：{content[:100]}")
        if thinking:
            print(f"  ⚠ thinking フィールドあり（長さ：{len(thinking)}）")
    else:
        print(f"✗ API エラー：{response.status_code}")
except Exception as e:
    print(f"✗ チャット API エラー：{e}")

# 3. 画像 OCR テスト（テスト画像を使用）
print("\n=== 画像 OCR テスト ===")
test_image_path = "test_red.png"
try:
    import os
    if os.path.exists(test_image_path):
        image = Image.open(test_image_path)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        payload = {
            "model": "qwen3.5:4b",
            "messages": [
                {"role": "system", "content": "You are a raw text extraction tool."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Extract all text from this image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            content = data.get("message", {}).get("content", "")
            thinking = data.get("message", {}).get("thinking", "")
            print(f"✓ 画像 OCR 成功")
            print(f"  コンテンツ：{content[:200] if content else 'None'}")
            if thinking:
                print(f"  ⚠ thinking フィールドあり（長さ：{len(thinking)}）")
        else:
            print(f"✗ 画像 OCR エラー：{response.status_code}")
            print(f"  レスポンス：{response.text[:200]}")
    else:
        print(f"⚠ テスト画像 {test_image_path} が見つかりません")
except Exception as e:
    print(f"✗ 画像 OCR エラー：{e}")

# 4. OpenAI 互換 API テスト
print("\n=== OpenAI 互換 API テスト ===")
try:
    from openai import OpenAI
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        timeout=120.0
    )
    
    response = client.chat.completions.create(
        model="qwen3.5:4b",
        messages=[{"role": "user", "content": "Test message via OpenAI API"}],
        extra_body={"stream": False}
    )
    content = response.choices[0].message.content
    print(f"✓ OpenAI 互換 API 成功")
    print(f"  コンテンツ：{content[:100] if content else 'None'}")
except Exception as e:
    print(f"✗ OpenAI 互換 API エラー：{e}")

print("\n=== テスト完了 ===")
