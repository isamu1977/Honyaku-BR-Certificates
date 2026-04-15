"""
BACKUP - Ollama Provider (Legacy two-step pipeline)
This file contains the original Ollama-based implementation using qwen3.5:2b for OCR
and mistral:instruct for JSON structuring/translation.
No longer used by default; kept for reference.
"""

import abc
import os
import json
import base64
import requests
import re
from io import BytesIO
from PIL import Image
from openai import OpenAI


PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")


def load_prompt(document_type):
    """
    Loads the appropriate prompt file based on document type.
    """
    if document_type == "BIRTH_NEW_VER1":
        filename = "birth_new.txt"
    elif document_type == "BIRTH_NEW_VER2":
        filename = "birth_new_v2.txt"
    elif document_type == "BIRTH_OLD":
        filename = "birth_old.txt"
    elif document_type == "BIRTH_STRICT":
        filename = "birth_strict.txt"
    elif document_type == "MARRIAGE_NEW_VER1":
        filename = "marriage_new.txt"
    elif document_type == "MARRIAGE_NEW_VER2":
        filename = "marriage_new_v2.txt"
    elif document_type == "MARRIAGE_OLD":
        filename = "marriage_old.txt"
    elif document_type == "MARRIAGE_STRICT":
        filename = "marriage_strict.txt"
    else:
        filename = "birth_new.txt"

    prompt_path = os.path.join(PROMPTS_DIR, filename)

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Prompt file not found: {prompt_path}")
        return ""


def clean_thinking_tags(text):
    """
    Remove thinking/reasoning tags from Qwen3.5 and other models that output reasoning.
    """
    if not text:
        return text

    # Remove <think>...</think> blocks
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove <think>...</think> blocks (Markdown-style)
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove "Thinking Process:" or similar headers followed by structured reasoning
    text = re.sub(r'Thinking Process:.*?(?=\n\n|\n[A-Z]|\{)', '', text, flags=re.DOTALL | re.IGNORECASE)

    return text.strip()


def normalize_birth_strict_data(data: dict) -> dict:
    """
    Normalize LLM output to match the official 19-key Birth Strict schema.
    Maps various key names to the standard keys.
    """
    # Official 19-key schema
    normalized = {
        "registrationNum": "",
        "name": "",
        "cpf": "",
        "gender": "",
        "birthDate": "",
        "birthTime": "",
        "birthPlace": "",
        "fatherInfo": "",
        "motherInfo": "",
        "paternalGrandparents": "",
        "maternalGrandparents": "",
        "twins": "",
        "twinsInfo": "",
        "registrationDate": "",
        "dnvs": "",
        "registrationNotes": "",
        "notaryOffice": "",
        "emissionDate": "",
        "scrivener": ""
    }

    # Key mappings (LLM might use variations)
    key_mappings = {
        "registrationNum": ["registrationNum", "matricula", "matriculaNumero", "registration_number", "登録番号"],
        "name": ["name", "nome", "registeredName", "氏名"],
        "cpf": ["cpf", "cpfNumero", "taxId", "個人納税者番号"],
        "gender": ["gender", "sexo", "sex", "性別"],
        "birthDate": ["birthDate", "dataNascimento", "birth_date", "生年月日"],
        "birthTime": ["birthTime", "horaNascimento", "birth_time", "出生時間"],
        "birthPlace": ["birthPlace", "localNascimento", "birth_place", "出生地"],
        "fatherInfo": ["fatherInfo", "father_name", "pai", "father", "父親"],
        "motherInfo": ["motherInfo", "mother_name", "mae", "mother", "母親"],
        "paternalGrandparents": ["paternalGrandparents", "grandparents_paternal", "父方祖父母"],
        "maternalGrandparents": ["maternalGrandparents", "grandparents_maternal", "母方祖父母"],
        "twins": ["twins", "gemios", "twins_status", "双子の有無"],
        "twinsInfo": ["twinsInfo", "gemiosInfo", "twins_data", "双子の情報"],
        "registrationDate": ["registrationDate", "dataRegistro", "registration_date", "登録日", "届出年月日"],
        "dnvs": ["dnvs", "dnvNumber", "dnv", "birth_certificate_number", "出生証明書番号"],
        "registrationNotes": ["registrationNotes", "annotations", "averbacoes", "notes", "備考", "記録"],
        "notaryOffice": ["notaryOffice", "cartorio", "notary", "自然人登記役場"],
        "emissionDate": ["emissionDate", "dataEmissao", "emission_date", "発行日"],
        "scrivener": ["scrivener", "escrivao", "registrar", "公証人", "筆記者"]
    }

    # Map keys from LLM output to standard schema
    for standard_key, variations in key_mappings.items():
        for variation in variations:
            if variation in data and data[variation]:
                normalized[standard_key] = str(data[variation]).strip()
                break

    return normalized


def safe_parse_json(text):
    """
    Safely parse JSON from AI response, handling markdown blocks, JavaScript exports, and common formatting issues.
    Returns the parsed dict or raises an exception with details.
    """
    if not text:
        raise ValueError("Empty response from AI")

    import ast
    original_text = text

    # Remove thinking/reasoning tags first
    text = clean_thinking_tags(text)
    text = text.strip()

    # Try to extract JSON from JavaScript export statement
    # Pattern: export const xxx = { ... } or export const xxx = {...}
    js_export_match = re.search(r'export\s+const\s+\w+\s*=\s*({.*?})\s*;?\s*$', text, re.DOTALL)
    if js_export_match:
        text = js_export_match.group(1)
        print("Extracted JSON from JavaScript export statement")

    # Remove markdown code blocks if present
    if text.startswith("```") or "```json" in text or "```" in text:
        match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            text = match.group(1).strip()

    # Remove any leading/trailing whitespace and newlines
    text = text.strip()

    # Try to find JSON object in the text (starts with { and ends with })
    if not text.startswith('{'):
        json_match = re.search(r'({.*})', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)

    # Fix trailing commas before closing braces/brackets
    text = re.sub(r',\s*([\]}])', r'\1', text)

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Fallback 1: Try using python's ast.literal_eval for single quotes
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, dict):
                return parsed
        except BaseException:
            pass

        # Fallback 2: Try quoting unquoted keys using regex
        try:
            fixed_text = re.sub(r'(?<!["\'])\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?=\s*:)', r'"\1"', text)
            return json.loads(fixed_text)
        except BaseException:
            pass

        print(f"JSON parsing error: {e}")
        print(f"Raw text (first 500 chars): {original_text[:500]}")
        print(f"Processed text (first 500 chars): {text[:500]}")
        raise


class OllamaProvider:
    """
    Legacy Ollama provider using two-step pipeline:
    Step 1: qwen3.5:2b for OCR text extraction (vision)
    Step 2: mistral:instruct for JSON structuring + Japanese translation
    """
    def __init__(self, model: str = None):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            timeout=300.0,
        )
        self.vision_model = "qwen3.5:2b"
        self.text_model = "mistral:instruct"

    def extract_text(self, image: Image.Image) -> str:
        max_size = 1024
        if image.width > max_size or image.height > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        if image.mode in ('LA', 'RGBA', 'P'):
            image = image.convert('RGB')

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        prompt = "Extract all text from this image exactly as it appears. Output only the raw text."

        try:
            print(f"Sending request to Ollama Vision API with model: {self.vision_model}")
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                temperature=0.0,
                max_tokens=2048,
                extra_body={
                    "options": {
                        "num_predict": 2048,
                    }
                },
            )
            result = response.choices[0].message.content
            print(f"Ollama raw response: {result}")
            extracted = clean_thinking_tags(result) if result else None
            print(f"\n=== TEXTO EXTRAÍDO DA IMAGEM (OLLAMA) ===\n{extracted}\n===========================================\n")
            return extracted
        except Exception as e:
            print(f"Error calling Ollama Vision: {str(e)}")
            raise ValueError(f"Ollama API Error: {str(e)}")

    def structure_data(self, extracted_text: str, schema_example: dict, document_type: str) -> dict:
        print(f"Manual document type selected: {document_type}")

        prompt_content = "/no_think\n" + load_prompt(document_type)
        if not prompt_content:
             prompt_content = f"/no_think\nExtract and structure the text into JSON matching this schema: {json.dumps(schema_example)}"

        prompt_content += "\n\nTranslate the extracted data into Japanese where appropriate (e.g., names, cities, states), and format the output as JSON. CRITICAL INSTRUCTION: DO NOT hallucinate or invent any names, dates, or data. If a field's information is not explicitly present in the extracted text, strictly output an empty string '' for that field."

        prompt_content += "\n\nDO NOT output any <think> reasoning tags. Just output the JSON object directly without any preamble."

        messages = [
            {"role": "system", "content": "You are a precise data extraction assistant that translates Brazilian Portuguese text into Japanese. You output strict JSON format. You NEVER invent or hallucinate data that is not in the source text. You NEVER output <think> tags or engage in extended reasoning."},
            {"role": "user", "content": f"{prompt_content}\n\nExtracted Text:\n{extracted_text}"}
        ]

        try:
            print(f"Sending request to Ollama Text API with model: {self.text_model}")
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=messages,
                temperature=0.0,
                response_format={"type": "json_object"},
                extra_body={
                    "stream": False,
                    "options": {
                        "num_predict": 2048,
                        "temperature": 0.0,
                        "format": "json",
                    }
                },
            )
            raw_response = response.choices[0].message.content
            print(f"\n=== TRADUÇÃO/ESTRUTURAÇÃO JSON (MISTRAL) ===\n{raw_response}\n===========================================\n")
            cleaned_response = clean_thinking_tags(raw_response) if raw_response else ""
            result = safe_parse_json(cleaned_response)

            if document_type == "BIRTH_STRICT":
                result = normalize_birth_strict_data(result)

            result["documentType"] = document_type
            return result
        except Exception as e:
            print(f"Error calling Ollama Text: {e}")
            return {"error": str(e), "documentType": document_type}
