import requests
import base64

b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="

# Test OpenAI standard
resp = requests.post("http://localhost:8080/v1/chat/completions", json={
    "model": "glm-ocr",
    "messages": [
        {"role": "user", "content": "Extract text", "images": [b64]}
    ]
})
print("Ollama style inside message:", resp.status_code, resp.text)

resp2 = requests.post("http://localhost:8080/v1/chat/completions", json={
    "model": "glm-ocr",
    "messages": [
        {"role": "user", "content": "Extract text"}
    ],
    "images": [b64]
})
print("Root level images:", resp2.status_code, resp2.text)

resp3 = requests.post("http://localhost:8080/v1/chat/completions", json={
    "model": "glm-ocr",
    "messages": [
        {"role": "user", "content": [{"type": "text", "text": "Extract text"}, {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}}]}
    ]
})
print("OpenAI standard:", resp3.status_code, resp3.text)

