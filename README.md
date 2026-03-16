# Honyaku BR Certificates - AI-Powered Document Translation System

A system that automatically extracts and translates data from Brazilian birth and marriage certificates using AI (Ollama), with inline editing capabilities and backup management.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Backup System](#backup-system)
- [Troubleshooting](#troubleshooting)

## Features

### Core Features

- **AI-Powered OCR**: Automatically extract text from images/PDFs using Ollama vision models (`qwen3.5:4b`)
- **Document Type Detection**: Automatically identifies document type (BIRTH_NEW, BIRTH_OLD, MARRIAGE_NEW)
- **Smart Translation**: Translates extracted text to Japanese with proper formatting rules
- **Inline Editing**: Click on any field to edit directly in the document view
- **Visual Feedback**: Edited fields are highlighted with yellow background and edit icon (✎)
- **Backup Management**: Save, load, and manage document backups
- **Multiple Document Types**: Supports birth certificates (new/old versions) and marriage certificates
- **Print-Ready**: Direct printing functionality with proper formatting

### Document Types Supported

- **Birth Certificate (New)**: Modern format with Matrícula number
- **Birth Certificate (Old)**: Old format with Livro/Folha numbers
- **Marriage Certificate (New)**: Modern marriage certificates

## Project Structure

```
honyaku-app/
├── front/                  # SvelteKit frontend application
│   ├── src/
│   │   ├── routes/          # Pages
│   │   ├── +page.svelte         # Main page with upload & backup list
│   │   ├── birthNewVersion/     # New birth certificate template
│   │   ├── birthOldVersion/     # Old birth certificate template
│   │   └── marryNewVersion/     # Marriage certificate template
│   │
│   │   ├── lib/
│   │   │   ├── components/       # Reusable components
│   │   │   │   ├── EditableField.svelte       # Inline editable field
│   │   │   │   ├── OneLineCell.svelte         # Single field cell
│   │   │   │   ├── TwoLinesCell.svelte         # Two fields cell
│   │   │   │   ├── TwoLinesCellGrand.svelte   # Grandparents cell (8 fields)
│   │   │   │   ├── TwoLinesCellSimple.svelte  # Simple two fields cell
│   │   │   │   ├── MarryTwoLinesCell.svelte    # Marriage cell
│   │   │   │   └── MarryTwoLinesCellCouple.svelte
│   │   │   └── TranslatorData.svelte     # Translation credits
│   │   │
│   │   ├── data/           # Static data templates
│   │   │   ├── birthNewVersionData.js
│   │   │   ├── birthOldVersionData.js
│   │   │   └── marryNewVersionData.js
│   │   │
│   │   └── stores/
│   │       └── certificationStore.js  # State management with backup functions
│   │
│   └── package.json
│
├── backend/                  # FastAPI backend application
│   ├── src/
│   │   ├── main.py           # FastAPI application & endpoints
│   │   └── services/
│   │       ├── pdf.py         # PDF to image conversion
│   │       ├── ai_providers.py # AI integration (text extraction & structuring)
│   │       └── __init__.py
│   │
│   ├── prompts/                # AI instruction prompts
│   │   ├── birth_new.txt     # BIRTH_NEW extraction instructions
│   │   ├── birth_old.txt     # BIRTH_OLD extraction instructions
│   │   └── marriage_new.txt  # MARRIAGE_NEW extraction instructions
│   │
│   ├── venv/                # Python virtual environment
│   └── requirements.txt       # Python dependencies
│
├── Backup/                  # Backup storage directory
│   ├── BirthNew/            # Birth certificate (new) backups
│   ├── BirthOld/            # Birth certificate (old) backups
│   └── MarriageNew/          # Marriage certificate backups
│
└── README.md                # This file
```

## Technologies

### Frontend
- **SvelteKit**: Web framework for building the application
- **Svelte**: Reactive UI components
- **TailwindCSS**: Utility-first CSS framework
- **JavaScript/ES6+**: Modern JavaScript features

### Backend
- **Python 3.12**: Backend runtime
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation using BaseModel
- **Pillow (PIL)**: Image processing
- **pdf2image**: PDF to image conversion
- **Requests**: HTTP client for AI REST API

### AI
- **Ollama**: Local AI inference engine
  - `qwen3.5:4b`: Vision model for text extraction
  - `mistral:instruct`: Text model for data structuring and translation
  - Alternative models: `llama3`, `phi3` available

## Architecture

### System Flow

```
┌─────────────┐
│   Frontend   │  SvelteKit Web App
└──────┬──────┘
       │
       │ HTTP (REST API)
       ▼
┌─────────────┐
│   Backend    │  FastAPI Server
└──────┬──────┘
       │
       ├──────────────────────┐
       │                      │
       ▼                      ▼
┌─────────────┐       ┌──────────┐
│   Ollama    │       │  PDF/Img │
│  Vision      │       │   Files   │
└──────┬───┘       └──────────┘
       │ Text Extraction
       ▼
┌─────────────────┐
│  Data JSON     │
└─────────────────┘
```

### Data Flow

1. **Upload**: Frontend sends image/PDF to backend
2. **Processing**: Backend converts to image (if PDF)
3. **Text Extraction**: Ollama vision model (`qwen3.5:4b`) extracts all text
4. **Data Structuring**: Ollama text model (`mistral:instruct`) translates and structures data into JSON
5. **State Management**: Data stored in Svelte store with original backup
6. **Display**: User sees document with extracted data
7. **Editing**: User clicks fields to edit inline
8. **Backup**: Edited data can be saved as backup file
9. **Load**: Previous backups can be loaded from storage

## Installation

### Prerequisites

- **Node.js 18+** (for frontend)
- **Python 3.12+** (for backend)
- **Ollama** (installed and running locally)
- **Poppler** (for PDF processing, optional if using images only)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Ollama is running**
   Ensure Ollama is active and the required models are pulled:
   ```bash
   ollama pull qwen3.5:4b
   ollama pull mistral:instruct
   ```

5. **Start backend server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd front
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:5173`

## Configuration

### Backend Configuration

Edit `backend/main.py` to configure:

```python
# Model configurations
VISION_MODEL = "qwen3.5:4b"      # Vision model for text extraction
TEXT_MODEL = "mistral:instruct"   # Text model for data structuring and translation

# Backup directories
BACKUP_DIR = "../Backup"
BACKUP_SUBDIRS = {
    "BIRTH_NEW": "BirthNew",
    "BIRTH_OLD": "BirthOld",
    "MARRIAGE_NEW": "MarriageNew"
}
```

### Frontend Configuration

No additional configuration required. The frontend automatically connects to the backend at `http://localhost:8000`.

### AI Models

**Available Ollama Models**:
- `qwen3.5:4b` - Recommended for text extraction
- `mistral:instruct` - Recommended for structuring and translation
- `llama3` - Alternative text model
- `phi3` - Lightweight alternative

## Usage

### Quick Start

1. **Start all services**:
   ```bash
   # Terminal 1: Backend
   cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2: Frontend
   cd front && npm run dev
   
   # Terminal 3: Local MLX Server (if not running on port 45389)
   # Run your native MLX start command

2. **Open browser**:
   Navigate to `http://localhost:5173`

3. **Upload document**:
   - Click on the upload area
   - Select an image (JPG, PNG) or PDF
   - Wait for AI processing (may take 10-30 seconds)

4. **Review extracted data**:
   - System automatically identifies document type
   - Redirects to appropriate document template
   - All fields are filled with extracted data

5. **Edit fields** (if needed):
   - Click on any field to edit
   - Type the corrected value
   - Press Enter to save or click away
   - Press Esc to cancel
   - Edited fields are highlighted in yellow

6. **Backup** (optional):
   - Click "バックアップ保存" (Save Backup) button
   - Data is saved as `.js` file in Backup/ folder

7. **Print**:
   - Click "印刷" (Print) button
   - Document opens in print dialog

### Editing Fields

**Edit any field directly in the document:**

1. Click on the field you want to edit
2. The field becomes an input box
3. Type the corrected value
4. Press Enter to save
5. Or click away from the field
6. Press Esc to cancel without saving

**Visual indicators:**
- Yellow background: Field has been modified
- ✎ icon: Field is editable
- Normal background: Field has original AI data

### Restoring Original Data

If you made a mistake and want to restore the original AI-extracted data:

1. Click "元に戻す" (Restore) button
2. Confirm the action
3. All fields revert to original data

### Managing Backups

**View previous backups:**
- Scroll to "バックアップ" section on home page
- See list of all saved backups with:
  - Person name
  - Document type (with color coding)
  - Modification date

**Load a backup:**
- Click on any backup in the list
- Data loads into store
- Automatically redirected to appropriate document page

**Delete a backup:**
- Click "削除" (Delete) button next to backup
- Confirm deletion
- Backup file is removed from storage

### Backup File Format

Backups are saved as JavaScript files with the following naming:

```
{YYYY}-{MM}-{DD}-{name}-{document_type}.js
```

Example: `2026-01-22-アリセ ガブリエレ アルベス-BIRTH_NEW.js`

File content:
```javascript
export const certificationData = {
    "documentType": "BIRTH_NEW",
    "name": "アリセ ガブリエレ アルベス",
    "birthDate": "2015年03月16日",
    ...
};
```

## API Endpoints

### Backend API

Base URL: `http://localhost:8000`

#### Upload Document
```http
POST /upload
Content-Type: multipart/form-data

Request:
- file: Image or PDF file

Response (200 OK):
{
    "documentType": "BIRTH_NEW|BIRTH_OLD|MARRIAGE_NEW",
    "name": "Japanese name",
    "birthDate": "2024年01月15日",
    ...
}

Error (400):
{
    "detail": "File must be an image or PDF"
}

Error (500):
{
    "detail": "Failed to extract text from image"
}
```

#### Save Backup
```http
POST /backup
Content-Type: application/json

Request:
{
    "data": {
        "documentType": "BIRTH_NEW",
        "name": "Name",
        "birthDate": "2024年01月15日",
        ...
    }
}

Response (200 OK):
{
    "success": true,
    "filename": "2026-01-22-Name-BIRTH_NEW.js",
    "path": "/path/to/Backup/BirthNew/file.js"
}
```

#### List Backups
```http
GET /backups

Response (200 OK):
[
    {
        "filename": "2026-01-22-Name-BIRTH_NEW.js",
        "documentType": "BIRTH_NEW",
        "name": "Name",
        "date": "2026",
        "createdAt": "2026-01-22T10:00:00.000Z",
        "modifiedAt": "2026-01-22T10:00:00.000Z"
    },
    ...
]
```

#### Load Backup
```http
GET /backup/{filename}

Response (200 OK):
{
    "documentType": "BIRTH_NEW",
    "name": "Name",
    ...
}

Error (404):
{
    "detail": "Backup file not found"
}
```

#### Delete Backup
```http
DELETE /backup/{filename}

Response (200 OK):
{
    "success": true,
    "message": "Backup deleted successfully"
}

Error (404):
{
    "detail": "Backup file not found"
}
```

#### Health Check
```http
GET /

Response (200 OK):
{
    "message": "Honyaku BR Certificates Backend is running"
}
```

## Backup System

### Storage Structure

```
Backup/
├── BirthNew/              # New birth certificate backups
│   ├── 2026-01-22-Name1-BIRTH_NEW.js
│   └── 2026-01-22-Name2-BIRTH_NEW.js
├── BirthOld/              # Old birth certificate backups
│   └── 2026-01-22-Name3-BIRTH_OLD.js
└── MarriageNew/           # Marriage certificate backups
    └── 2026-01-22-Name4-MARRIAGE_NEW.js
```

### Backup Operations

**Create backup:**
- Automatic through UI (Save button)
- Stored as `.js` export file
- Includes all document fields
- Filename format: `YYYY-MM-DD-{name}-{type}.js`

**Load backup:**
- Click on backup in list
- Data loads into certification store
- Automatic redirect to document page
- Original data preserved for restore

**Delete backup:**
- Delete button next to each backup
- Confirmation required
- File permanently removed

### Data Persistence

- **Session data**: Stored in Svelte store (in-memory)
- **Original data**: Preserved for restore functionality
- **Backups**: Stored as files in Backup/ directory
- **No database**: All data is file-based

### Original vs Edited Data

The system maintains a copy of the original AI-extracted data separately from the current (potentially edited) data:

- **Original data**: What the AI initially extracted
- **Current data**: What you see (may include edits)
- **Restore**: Reverts current data to original data
- **Save backup**: Saves current data (including edits)

## Translation Rules

The AI follows specific formatting rules based on the document type:

### Name Formatting
- Convert Portuguese names to Katakana
- Use spaces between name parts (no ・ symbol)
- Preserve original name order

### Location Formatting
- Cities: Add 市 after city name
  - Example: "São Paulo" → "サンパウロ市"
- States: Add 州 after state name
  - Example: "São Paulo" → "サンパウロ州"
- Notary: Add 自然人登記役場 after notary name

### Date Formatting
- Use Japanese date format: YYYY年MM月DD日
- Birth dates with "生まれ": YYYY年MM月DD日生まれ

### Gender
- Masculine: 男性
- Feminine: 女性

### Twins
- Yes: 有り
- No: 無し

### Special Fields (Old Version)
- Registration number: Format as "XX番 YYページ ZZ冊"
- Use "出身" after birth places

## Troubleshooting

### Backend Issues

**Problem**: Backend won't start
```
Solution:
- Check port 8000 is not in use
- Verify Python 3.12+ is installed
- Check dependencies are installed: pip list
- Run: source venv/bin/activate && pip install -r requirements.txt
```

**Problem**: Text extraction returns null
```
Solution:
- Verify Local MLX is running with the required models (e.g., glm-ocr, translategemma-12b-4bit) loaded over port 45389.
- Increase model timeout in request
```

### Frontend Issues

**Problem**: Frontend won't start
```
Solution:
- Check Node.js version: node --version (should be 18+)
- Delete node_modules and reinstall: rm -rf node_modules && npm install
- Check port 5173 is not in use
```

**Problem**: Upload returns 500 error
```
Solution:
- Check backend is running: curl http://localhost:8000/
- Check backend logs in terminal
- Verify file is image or PDF
- Check PDF processing (requires Poppler)
```

**Problem**: Cannot edit fields
```
Solution:
- Refresh the page
- Check JavaScript console for errors
- Verify EditableField component is properly imported
```

### PDF Processing Issues

**Problem**: PDF to image conversion fails
```
Solution:
- Install Poppler (required for pdf2image):
  - macOS: brew install poppler
  - Linux: sudo apt-get install poppler-utils
  - Windows: Download and add to PATH
- Restart backend server
```

**Alternative**: Use only images (JPG, PNG)

## Development

### Running in Development Mode

**Backend**:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm run dev
```

### Project File Locations

- **Backend**: `/backend/main.py`
- **Prompts**: `/backend/prompts/*.txt`
- **Frontend**: `/front/src/routes/+page.svelte`
- **Components**: `/frontend/src/lib/components/*.svelte`
- **Store**: `/frontend/src/lib/stores/certificationStore.js`

### Adding New Document Types

1. Create prompt file in `backend/prompts/`
2. Add document type constant in `backend/main.py`
3. Create template page in `frontend/src/routes/`
4. Add data template in `frontend/src/lib/data/`
5. Update routing logic in `frontend/src/routes/+page.svelte`

### Modifying AI Instructions

Edit prompt files in `backend/prompts/`:
- `birth_new.txt` - New birth certificate instructions
- `birth_old.txt` - Old birth certificate instructions
- `marriage_new.txt` - Marriage certificate instructions

Add new extraction rules, formatting guidelines, or field mappings.

## File Naming Conventions

- **Python files**: `snake_case.py` (e.g., `pdf.py`, `ai_providers.py`)
- **Svelte files**: `PascalCase.svelte` (e.g., `OneLineCell.svelte`)
- **JavaScript files**: `camelCase.js` (e.g., `certificationStore.js`)
- **Backup files**: `YYYY-MM-DD-{name}-{type}.js`

## License

This is a personal project for document translation and data extraction.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all services are running (Backend, Frontend, Local MLX)
3. Check browser console for JavaScript errors
4. Check backend terminal for Python errors

## Version History

- **v1.0**: Initial release
  - AI-powered text extraction
  - Document type detection
  - Inline editing
  - Backup system
  - Three document types supported

---

**Built with SvelteKit, FastAPI, and Local MLX AI**
