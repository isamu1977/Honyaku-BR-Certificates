import requests
import base64

b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="

payloads = {
    "string_content_plus_images_in_message": {
        "model": "glm-ocr",
        "messages": [
            {"role": "user", "content": "Extract text", "images": [b64]}
        ]
    },
    "string_content_plus_images_at_root": {
        "model": "glm-ocr",
        "messages": [
            {"role": "user", "content": "Extract text"}
        ],
        "images": [b64]
    },
    "openai_standard": {
        "model": "glm-ocr",
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "Extract text"}, 
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]}
        ]
    },
    "markdown_image_in_content": {
        "model": "glm-ocr",
        "messages": [
            {"role": "user", "content": f"Extract text\n![image](data:image/jpeg;base64,{b64})"}
        ]
    }
}

for name, payload in payloads.items():
    try:
        resp = requests.post("http://localhost:8080/v1/chat/completions", json=payload, timeout=5)
        print(f"--- {name} ---")
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"--- {name} ERROR ---")
        print(e)
