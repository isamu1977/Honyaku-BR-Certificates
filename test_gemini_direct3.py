import sys
import os
import io

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from services.ai_providers import get_provider
from main import SCHEMA_EXAMPLE
from PIL import Image

try:
    provider = get_provider('gemini')
    print("Provider loaded.")

    extracted_text = "Certidão de Nascimento. Nome: Isamu. Pai: Roberto. Mãe: Maria."
    print("Testing structure_data with Gemini...")
    
    res = provider.structure_data(extracted_text, SCHEMA_EXAMPLE)
    print("Structured Result:")
    import json
    print(json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    import traceback
    traceback.print_exc()
