# MLX Inference Server - Complete Manual

Unified Local Inference Server using **Apple MLX** for M1/M2/M3 chips.

Compatible with the **OpenAI API**, allowing direct use of official SDKs in frontend applications (SvelteKit, React, etc.) and backend.

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Installation & Startup](#-installation--startup)
3. [Available Endpoints](#-available-endpoints)
4. [Available Models](#-available-models)
5. [Usage Guide by Feature](#-usage-guide-by-feature)
6. [Usage via cURL (Command Line)](#-usage-via-curl-command-line)
7. [Memory Management](#-memory-management)
8. [CORS Configuration](#-cors-configuration)
9. [Health Check & Monitoring](#-health-check--monitoring)
10. [Troubleshooting](#-troubleshooting)

---

## 🚀 Overview

This server provides a unified local API for:

| Category | Feature | Endpoint |
|----------|---------|----------|
| **Chat** | Text and multimodal (OCR, vision) | `/v1/chat/completions` |
| **Embeddings** | Multilingual semantic vectors | `/v1/embeddings` |
| **Audio - Transcription** | Speech-to-Text (ASR) | `/v1/audio/transcriptions` |
| **Audio - Synthesis** | Text-to-Speech (TTS) | `/v1/audio/speech` |
| **Images** | Generation via ComfyUI (proxy) | `/v1/images/generations` |
| **Music** | Music audio generation | `/v1/audio/music-generations` |

### Advantages

- ✅ **OpenAI Compatible**: Use official SDKs without modifications
- ✅ **100% Local**: No API costs, no external network latency
- ✅ **Privacy**: Your data never leaves your machine
- ✅ **Smart Memory Management**: Automatically loads/unloads models

---

## 📦 Installation & Startup

### Prerequisites

- macOS with Apple Silicon chip (M1/M2/M3)
- Python 3.10+
- Virtual environment already configured in `.venv/`

### Step 1: Activate Virtual Environment

```bash
cd /Users/isamumatsuyama/Documents/development/mlx-models
source .venv/bin/activate
```

### Step 2: Install Dependencies (if needed)

```bash
pip install -r server/requirements.txt
```

### Step 3: Start the Server

```bash
# From project root
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 4: Verify Server is Running

```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

**Server available at:** `http://localhost:8000`

---

## 🔌 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Server health check |
| `GET` | `/v1/models` | List models loaded in memory |
| `POST` | `/v1/chat/completions` | Chat with LLMs (text or multimodal) |
| `POST` | `/v1/embeddings` | Generate vector embeddings |
| `POST` | `/v1/audio/transcriptions` | Transcribe audio to text |
| `POST` | `/v1/audio/speech` | Convert text to speech |
| `POST` | `/v1/images/generations` | Generate images (requires ComfyUI) |
| `POST` | `/v1/audio/music-generations` | Generate music (currently mock) |

---

## 🧠 Available Models

### Original Models (`./original_models/`)

| Model Path | Type | Recommended Use |
|------------|------|-----------------|
| `./original_models/bge-m3` | Embeddings | Semantic search, RAG |
| `./original_models/Qwen3-ASR-1.7B` | Audio Transcription | Speech-to-Text in multiple languages |
| `./original_models/Qwen3-TTS-12Hz-1.7B-Base` | Speech Synthesis | Natural Text-to-Speech |

### Quantized 4-bit Models (`./quantized_models/`)

| Model Path | Type | Recommended Use |
|------------|------|-----------------|
| `./quantized_models/Qwen3.5-0.8B-4bit` | LLM | Fast tasks, low memory usage |
| `./quantized_models/Qwen3.5-4B-4bit` | LLM | **Recommended default** - balance of performance/memory |
| `./quantized_models/Qwen3.5-9B-4bit` | LLM | Complex tasks, higher accuracy |
| `./quantized_models/Qwen3.5-27B-4bit` | LLM | Very complex tasks (requires lots of memory) |
| `./quantized_models/GLM-4.7-Flash-4bit` | LLM | Fast and efficient chat |
| `./quantized_models/GLM-OCR-4bit` | Vision/OCR | Read text from images, documents |
| `./quantized_models/Phi-4-reasoning-vision-15B-4bit` | Multimodal LLM | Reasoning + vision |
| `./quantized_models/translategemma-12b-it-4bit` | Translation | Translation between languages |

---

## 📖 Usage Guide by Feature

### 1. Chat with LLM (Text)

#### Basic Example

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # No authentication required locally
)

response = client.chat.completions.create(
    model="./quantized_models/Qwen3.5-4B-4bit",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain what digital tarot is."}
    ],
    temperature=0.7,
)

print(response.choices[0].message.content)
```

#### Chat with Streaming (Real-time Response)

```python
stream = client.chat.completions.create(
    model="./quantized_models/Qwen3.5-4B-4bit",
    messages=[{"role": "user", "content": "Tell a short story."}],
    stream=True,  # Enable streaming
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

#### Available Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | (required) | Model path |
| `messages` | array | (required) | List of messages |
| `temperature` | float | 0.7 | Creativity (0-2) |
| `top_p` | float | 1.0 | Nucleus sampling (0-1) |
| `max_tokens` | int | null | Maximum tokens in response |
| `stream` | boolean | false | Enable streaming |
| `stop` | string/array | null | Stop sequences |
| `presence_penalty` | float | 0 | Penalty for new topics (-2 to 2) |
| `frequency_penalty` | float | 0 | Penalty for repetition (-2 to 2) |

---

### 2. Multimodal Chat (OCR / Vision)

Use for analyzing images, documents, charts, etc.

```python
import base64

# Load image and convert to base64
with open("document.png", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="./quantized_models/GLM-OCR-4bit",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Transcribe this document in Japanese."},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
        ]
    }]
)

print(response.choices[0].message.content)
```

---

### 3. Embeddings (Semantic Vectors)

#### Single Text

```python
embedding = client.embeddings.create(
    model="./original_models/bge-m3",
    input="Text to search semantically"
)

# Access vector
vector = embedding.data[0].embedding
print(f"Dimensions: {len(vector)}")
```

#### Multiple Texts (Batch)

```python
embeddings = client.embeddings.create(
    model="./original_models/bge-m3",
    input=[
        "News about Japanese culture",
        "Article about Japanese culture",
        "記事：日本の文化について",
        "Article about Japanese culture"
    ]
)

# Access all vectors
for data in embeddings.data:
    print(f"Index {data.index}: {len(data.embedding)} dimensions")
```

#### Available Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | (required) | Model path |
| `input` | string/array | (required) | Text(s) for embedding |
| `encoding_format` | string | "float" | Vector format ("float" or "base64") |

---

### 4. Audio Transcription (ASR)

```python
with open("audio.wav", "rb") as f:
    transcription = client.audio.transcriptions.create(
        model="./original_models/Qwen3-ASR-1.7B",
        file=f,
        language="ja",  # Japanese (optional - auto-detects)
        response_format="json"  # json, text, srt, verbose_json
    )

print(transcription.text)
```

#### Response Formats

| Format | Description |
|--------|-------------|
| `json` | JSON with text and metadata |
| `text` | Transcribed text only |
| `srt` | Subtitles in SRT format |
| `verbose_json` | Detailed JSON with segments and timestamps |

#### Available Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file` | file | (required) | Audio file |
| `model` | string | (required) | ASR model path |
| `language` | string | null | Language code (e.g., `ja`, `pt`, `en`, `zh`) |
| `prompt` | string | null | Optional prompt to guide transcription |
| `response_format` | string | "json" | Response format |
| `temperature` | float | 0 | Sampling temperature |

---

### 5. Text-to-Speech (TTS)

```python
response = client.audio.speech.create(
    model="./original_models/Qwen3-TTS-12Hz-1.7B-Base",
    input="こんにちは、これは音声合成のテストです。",
    voice="default",
    speed=1.0,
    response_format="mp3"
)

# Save audio
with open("output.mp3", "wb") as f:
    f.write(response.content)
```

#### Supported Audio Formats

| Format | Content-Type |
|--------|--------------|
| `mp3` | audio/mpeg |
| `opus` | audio/opus |
| `aac` | audio/aac |
| `flac` | audio/flac |
| `wav` | audio/wav |
| `pcm` | audio/pcm |

#### Available Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | (required) | TTS model path |
| `input` | string | (required) | Text to synthesize |
| `voice` | string | "default" | Voice identifier |
| `speed` | float | 1.0 | Speed (0.25 to 4.0) |
| `response_format` | string | "mp3" | Audio format |

---

### 6. Image Generation (ComfyUI)

**Requirement:** ComfyUI running at `http://127.0.0.1:8188`

```python
response = client.images.generate(
    model="sd15",
    prompt="A beautiful Japanese garden with cherry blossoms, digital art",
    n=1,
    size="1024x1024",
    response_format="b64_json",
)

# Decode and save image
import base64
image_data = response.data[0].b64_json
image_bytes = base64.b64decode(image_data)

with open("generated_image.png", "wb") as f:
    f.write(image_bytes)
```

#### Configure ComfyUI

```bash
# Install ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt

# Start ComfyUI server
python main.py --listen 127.0.0.1 --port 8188
```

---

### 7. Music Generation (Mock)

**Note:** This endpoint returns mock audio for development. Implement ACE-Step or YuE for real generation.

```python
response = client.post(
    "/v1/audio/music-generations",
    json={
        "prompt": "A calm Japanese jazz piece with piano and saxophone",
        "model": "ace-step",
        "duration": 30,
        "response_format": "b64_json"
    }
)

# Access audio as base64
audio_data = response.json()["data"][0]["b64_json"]
audio_bytes = base64.b64decode(audio_data)

with open("generated_music.wav", "wb") as f:
    f.write(audio_bytes)
```

---

## 💻 Usage via cURL (Command Line)

### Chat

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "./quantized_models/Qwen3.5-4B-4bit",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Embeddings

```bash
curl -X POST http://localhost:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "./original_models/bge-m3",
    "input": "Text for embedding"
  }'
```

### Audio Transcription

```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=./original_models/Qwen3-ASR-1.7B" \
  -F "language=ja"
```

### Text-to-Speech

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "./original_models/Qwen3-TTS-12Hz-1.7B-Base",
    "input": "こんにちは",
    "response_format": "mp3"
  }' \
  --output speech.mp3
```

### Health Check

```bash
curl http://localhost:8000/health
```

### List Loaded Models

```bash
curl http://localhost:8000/v1/models
```

---

## 🧠 Memory Management

The server implements **intelligent memory management** for Apple Silicon chips:

### How It Works

1. **One model per type**: Only one LLM, one VLM, etc. loaded at a time
2. **Automatic unload**: When loading a new model of the same type, the previous one is removed
3. **Complete cleanup**: Python GC + Metal cache are cleaned after unloading

### Why This Matters

This allows running large models (e.g., Qwen 27B) and then switching to OCR without out-of-memory (OOM) errors.

### Monitor Memory Usage

```bash
# Using macOS Activity Monitor
# Apple Menu > About This Mac > Memory > Activity Monitor

# Or via terminal (shows Python memory usage)
ps -o pid,rss,command -p $(pgrep -f "uvicorn|python")
```

### Recommendations by Model

| Model | Minimum Recommended Memory |
|-------|---------------------------|
| Qwen3.5-0.8B-4bit | 4 GB |
| Qwen3.5-4B-4bit | 8 GB |
| Qwen3.5-9B-4bit | 16 GB |
| Qwen3.5-27B-4bit | 32+ GB |

---

## 🌐 CORS Configuration

The server is already configured to accept requests from:

| Origin | Use |
|--------|-----|
| `http://localhost:3000` | Next.js, SvelteKit (default) |
| `http://localhost:3001` | Alternative ports |
| `http://localhost:5173` | Vite (React, Vue, Svelte) |
| `http://localhost:8080` | Other dev servers |

### Add New Origins

Edit `server/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://your-new-host:port",  # Add here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔍 Health Check & Monitoring

### Check Server Status

```bash
curl http://localhost:8000/health
# Returns: {"status": "healthy"}
```

### List Loaded Models

```bash
curl http://localhost:8000/v1/models
# Returns: {"object": "list", "data": [{"id": "...", "type": "..."}]}
```

### Interactive Documentation (Swagger UI)

Access in browser: `http://localhost:8000/docs`

---

## 📁 Project Structure

```
server/
├── main.py                   # Main FastAPI application
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
├── core/
│   └── model_manager.py      # Model manager with unloading
├── schemas/
│   ├── chat.py               # OpenAI schemas for chat
│   ├── embeddings.py         # OpenAI schemas for embeddings
│   ├── audio.py              # OpenAI schemas for audio
│   ├── images.py             # OpenAI schemas for images
│   └── music.py              # Custom schemas for music
├── routes/
│   ├── chat.py               # Chat/completions routes
│   ├── embeddings.py         # Embeddings routes
│   ├── audio.py              # Audio routes (TTS/ASR)
│   ├── images.py             # Image routes (ComfyUI proxy)
│   └── music.py              # Music routes (mock)
└── services/
    ├── llm_service.py        # LLM service (mlx-lm)
    ├── vlm_service.py        # VLM service (mlx-vlm)
    ├── embedding_service.py  # Embedding service
    ├── asr_service.py        # ASR service
    ├── tts_service.py        # TTS service
    ├── comfyui_service.py    # ComfyUI proxy
    └── music_service.py      # Music service (mock)
```

---

## 🛠️ Troubleshooting

### Error: "No module named 'mlx_lm'"

```bash
pip install mlx-lm
```

### Error: "Out of memory"

1. Unload models manually:
   ```bash
   curl -X DELETE http://localhost:8000/v1/models/unload
   ```
2. Use smaller or more quantized models
3. Close other applications using GPU

### CORS Errors in Frontend

- Verify dev server origin is in `allow_origins` list
- Use `http://` not `https://` for local development
- Clear browser cache

### Model Takes Long to Load

- **First load** is always slower (model being read from disk)
- **Subsequent loads** are faster (cached)
- Use 4-bit quantized models for better performance

### Server Won't Start

```bash
# Check if port is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>

# Restart server
uvicorn server.main:app --host 0.0.0.0 --port 8000
```

---

## ⚠️ Important Notes

1. **Model paths**: Use relative paths from project root or absolute paths
2. **First request**: May take a few seconds (model loading into RAM)
3. **Unified memory**: Monitor usage in `Activity Monitor` → `Memory Pressure`
4. **Quantized models**: Use 4-bit versions for better performance with limited memory
5. **API Key**: No authentication required locally (`api_key="not-needed"`)

---

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Apple MLX](https://github.com/ml-explore/mlx)
- [MLX LM](https://github.com/ml-explore/mlx-examples/tree/main/llms)
- [MLX VLM](https://github.com/Blaizzy/mlx-vlm)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
