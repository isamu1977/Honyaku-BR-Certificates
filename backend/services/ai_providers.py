import abc
import os
import json
import re
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")

# Gemini 2.5 Flash model name
GEMINI_MODEL = "gemini-2.5-flash"


def load_prompt(document_type):
    """
    Loads the appropriate prompt file based on document type.
    """
    prompt_files = {
        "BIRTH_NEW_VER1": "birth_new.txt",
        "BIRTH_NEW_VER2": "birth_new_v2.txt",
        "BIRTH_OLD": "birth_old.txt",
        "BIRTH_STRICT": "birth_strict.txt",
        "MARRIAGE_NEW_VER1": "marriage_new.txt",
        "MARRIAGE_NEW_VER2": "marriage_new_v2.txt",
        "MARRIAGE_OLD": "marriage_old.txt",
        "MARRIAGE_STRICT": "marriage_strict.txt",
    }

    filename = prompt_files.get(document_type, "birth_new.txt")
    prompt_path = os.path.join(PROMPTS_DIR, filename)

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Prompt file not found: {prompt_path}")
        return ""


class AIProvider(abc.ABC):
    @abc.abstractmethod
    def process_image(self, image: Image.Image, document_type: str) -> dict:
        """Single-step multimodal processing: image + prompt -> JSON"""
        pass


class GeminiProvider(AIProvider):
    """
    Gemini 2.5 Pro provider using a single multimodal call.
    Sends the image and structured prompt together, forcing JSON output
    via response_mime_type='application/json'.
    """
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def process_image(self, image: Image.Image, document_type: str) -> dict:
        print(f"Processing image with Gemini 2.5 Pro (document_type={document_type})")

        # Load the document-type-specific prompt
        prompt_content = load_prompt(document_type)
        if not prompt_content:
            prompt_content = f"Extract and structure the data from this Brazilian certificate image into JSON matching the expected schema for document type: {document_type}"

        # Add translation and anti-hallucination instructions
        full_prompt = (
            f"{prompt_content}\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "- Translate all appropriate fields (names, places, etc.) into Japanese.\n"
            "- DO NOT hallucinate or invent any names, dates, or data.\n"
            "- If a field's information is not explicitly present in the image, strictly output an empty string '' for that field.\n"
            "- Output valid JSON only, with no markdown code blocks or preamble.\n"
        )

        # Force JSON output via generation config
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json"
        )

        try:
            # Single multimodal call: image + text prompt together
            response = self.model.generate_content(
                [full_prompt, image],
                generation_config=generation_config,
            )

            raw_response = response.text
            print(f"Gemini raw response (first 500 chars): {raw_response[:500]}")

            result = safe_parse_json(raw_response)
            result["documentType"] = document_type
            return result

        except Exception as e:
            print(f"Error calling Gemini 2.5 Pro: {e}")
            return {"error": str(e), "documentType": document_type}


def safe_parse_json(text):
    """
    Safely parse JSON from AI response, handling markdown blocks, JavaScript exports, and common formatting issues.
    Returns the parsed dict or raises an exception with details.
    """
    if not text:
        raise ValueError("Empty response from AI")

    import ast
    original_text = text
    text = text.strip()

    # Try to extract JSON from JavaScript export statement
    js_export_match = re.search(r'export\s+const\s+\w+\s*=\s*({.*?})\s*;?\s*$', text, re.DOTALL)
    if js_export_match:
        text = js_export_match.group(1)
        print("Extracted JSON from JavaScript export statement")

    # Remove markdown code blocks if present
    if text.startswith("```") or "```json" in text or "```" in text:
        match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            text = match.group(1).strip()

    text = text.strip()

    # Try to find JSON object in the text
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


def get_provider(name: str, model: str = None) -> AIProvider:
    if name.lower() == "gemini":
        return GeminiProvider()
    else:
        # Default to Gemini if unknown provider
        return GeminiProvider()
