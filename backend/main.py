from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from services import pdf, ai_providers
from routes import backend_control_router
from PIL import Image
import io
import json
import os
import datetime
import shutil
import socket
from pydantic import BaseModel

app = FastAPI()

# バックエンド制御ルーターを登録
app.include_router(backend_control_router)

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

# ... (CORS and Backup config remain the same) ...

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Backup configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(BASE_DIR, "Backup")
BACKUP_SUBDIRS = {
    "BIRTH_NEW": "BirthNew",
    "BIRTH_OLD": "BirthOld",
    "BIRTH_STRICT": "BirthNew",
    "MARRIAGE_NEW": "MarriageNew",
    "MARRIAGE_OLD": "MarriageNew",
    "MARRIAGE_STRICT": "MarriageNew"
}

# Ensure backup directories exist
for subdir in BACKUP_SUBDIRS.values():
    os.makedirs(os.path.join(BACKUP_DIR, subdir), exist_ok=True)

class BackupData(BaseModel):
    data: dict

# New Official Schema - 19 keys for Birth Certificate (Strict Format)
class BirthCertificationData(BaseModel):
    registrationNum: str = ""
    name: str = ""
    cpf: str = ""
    gender: str = ""
    birthDate: str = ""
    birthTime: str = ""
    birthPlace: str = ""
    fatherInfo: str = ""
    motherInfo: str = ""
    paternalGrandparents: str = ""
    maternalGrandparents: str = ""
    twins: str = ""
    twinsInfo: str = ""
    registrationDate: str = ""
    dnvs: str = ""
    registrationNotes: str = ""
    notaryOffice: str = ""
    emissionDate: str = ""
    scrivener: str = ""
    
    # Translator info (added separately, not from LLM)
    translatorName: str = ""
    translatorAddress: str = ""
    translatorPhone: str = ""
    
    # Document type for routing
    documentType: str = "BIRTH_STRICT"

# Combined Schema Example
SCHEMA_EXAMPLE = {
    "documentType": "BIRTH_NEW, BIRTH_OLD, MARRIAGE_NEW, MARRIAGE_OLD",
    "titleAditional1": "",
    "titleAditional2": "",
    "registrationNum": "123456... or Livro X Folha Y",
    "registrationDate": "YYYY年MM月DD日",
    "notaryCity": "",
    "notaryState": "",
    "notaryName": "",
    "mainsScrivenerName": "",
    "emissionDate": "YYYY年MM月DD日",
    "scrivenerSignName": "",
    "scrivenerType": "",
    
    # Birth Fields
    "name": "Nome Completo (Birth)",
    "birthDate": "YYYY年MM月DD日",
    "birthTime": "HH:MM",
    "birthCityState": "",
    "registrationPlace": "",
    "birthPlace": "",
    "gender": "男性/女性",
    "fatherName": "",
    "motherName": "",
    "fatherSideGrandFather": "",
    "fatherSideGrandMother": "",
    "motherSideGrandFather": "",
    "motherSideGrandMother": "",
    "twins": "無し/有り",
    "twinBrotherName": "-",
    "newBornNumber": "",
    "registrationChange": "",
    "registrationAditionalInfo": "",
    
    # Old Version Fields
    "registrationPerson": "",
    "otherRegistration": "",

    # Marriage Fields
    "husbandSingleName": "",
    "husbandKojinBango": "",
    "wifeSingleName": "",
    "wifeKojinBango": "",
    "husbandName": "",
    "husbandBirthDate": "",
    "husbandBirthPlace": "",
    "husbandCitizenship": "",
    "husbandFatherName": "",
    "husbandMotherName": "",
    "wifeName": "",
    "wifeBirthDate": "",
    "wifeBirthPlace": "",
    "wifeCitizenship": "",
    "wifeFatherName": "",
    "wifeMotherName": "",
    "marryCondition": "Comunhão/Separação...",
    "husbandMarriedName": "",
    "wifeMarriedName": ""
}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    provider: str = Form("ollama"),
    model: str = Form("qwen3.5:4b"),
    document_type: str = Form(...)
):
    content_type = file.content_type or ""
    if not content_type.startswith("image/") and content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be an image or PDF")

    contents = await file.read()
    image = None

    try:
        if content_type == "application/pdf":
            # Convert first page of PDF to image
            images = pdf.convert_pdf_to_images(contents)
            if images:
                image = images[0]
            else:
                 raise HTTPException(status_code=400, detail="Could not convert PDF to image")
        else:
            image = Image.open(io.BytesIO(contents))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    if image:
        try:
            ai_service = ai_providers.get_provider(provider, model)
            print(f"\n>>> INICIANDO EXTRAÇÃO - Provider: {provider}, Model: {model}")
            
            # Step 1: Extract Text
            extracted_text = ai_service.extract_text(image)
            if not extracted_text:
                 raise HTTPException(status_code=500, detail=f"Failed to extract text from image using {provider}")
                 
            # Step 2: Structure Data
            structured_data = ai_service.structure_data(extracted_text, SCHEMA_EXAMPLE, document_type)
            
            if not structured_data:
                structured_data = {}
            
            return structured_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in AI processing: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Honyaku BR Certificates Backend is running"}

@app.post("/backup")
async def save_backup(backup: BackupData):
    try:
        data = backup.data
        document_type = data.get("documentType", "BIRTH_NEW")
        subdir = BACKUP_SUBDIRS.get(document_type, "BirthNew")
        
        # Generate filename
        name = data.get("name", "") or data.get("husbandName", "") or data.get("wifeName", "") or "unknown"
        name_clean = "".join(c for c in name if c.isalnum() or c in " -_").strip()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}-{name_clean}-{document_type}.js"
        filepath = os.path.join(BACKUP_DIR, subdir, filename)
        
        # Write backup file
        export_content = "export const certificationData = " + json.dumps(data, indent=2, ensure_ascii=False) + ";"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(export_content)
        
        return {"success": True, "filename": filename, "path": filepath}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving backup: {str(e)}")

@app.get("/backups")
async def list_backups():
    try:
        backups = []
        
        for doc_type, subdir in BACKUP_SUBDIRS.items():
            dirpath = os.path.join(BACKUP_DIR, subdir)
            if not os.path.exists(dirpath):
                continue
                
            for filename in os.listdir(dirpath):
                if filename.endswith(".js"):
                    filepath = os.path.join(dirpath, filename)
                    stat = os.stat(filepath)
                    created_time = datetime.datetime.fromtimestamp(stat.st_ctime)
                    modified_time = datetime.datetime.fromtimestamp(stat.st_mtime)
                    
                    # Extract name from filename
                    # Format: YYYY-MM-DD-name-type.js
                    parts = filename.replace(".js", "").split("-")
                    if len(parts) >= 3:
                        file_date = parts[0]
                        file_name = "-".join(parts[1:-1])
                    else:
                        file_date = ""
                        file_name = filename
                    
                    backups.append({
                        "filename": filename,
                        "documentType": doc_type,
                        "name": file_name,
                        "date": file_date,
                        "createdAt": created_time.isoformat(),
                        "modifiedAt": modified_time.isoformat()
                    })
        
        # Sort by modified date descending
        backups.sort(key=lambda x: x["modifiedAt"], reverse=True)
        return backups
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing backups: {str(e)}")

@app.get("/backup/{filename}")
async def load_backup(filename: str):
    try:
        # Search in all backup subdirectories
        for subdir in BACKUP_SUBDIRS.values():
            filepath = os.path.join(BACKUP_DIR, subdir, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Extract JSON from export statement
                    if "export const certificationData = " in content:
                        json_str = content.replace("export const certificationData = ", "").rstrip(";")
                        data = json.loads(json_str)
                        return data
                    else:
                        json_str = content.rstrip(";")
                        return json.loads(json_str)
        
        raise HTTPException(status_code=404, detail="Backup file not found")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing backup file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading backup: {str(e)}")

@app.delete("/backup/{filename}")
async def delete_backup(filename: str):
    try:
        # Search in all backup subdirectories
        for subdir in BACKUP_SUBDIRS.values():
            filepath = os.path.join(BACKUP_DIR, subdir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return {"success": True, "message": "Backup deleted successfully"}
        
        raise HTTPException(status_code=404, detail="Backup file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting backup: {str(e)}")
