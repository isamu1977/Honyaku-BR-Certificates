import sys
import os
import io

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from services.ai_providers import get_provider
from PIL import Image

try:
    provider = get_provider('gemini')
    print("Provider loaded.")
    # Open the real image created
    image = Image.open('test_red.png')
    print("Image loaded, extracting text...")
    
    res = provider.extract_text(image)
    print("Result:")
    print(res)
except Exception as e:
    import traceback
    traceback.print_exc()
