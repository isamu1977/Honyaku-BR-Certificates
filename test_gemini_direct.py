import sys
import os
import io

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from services.ai_providers import get_provider
from PIL import Image

try:
    provider = get_provider('gemini')
    print("Provider loaded.")
    # Create dummy 1x1 image
    empty_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa74B\x12\x00\x00\x00\x00IEND\xaeB`\x82'
    image = Image.open(io.BytesIO(empty_image))
    print("Image loaded, extracting text...")
    
    # We will temporarily mock the API key if it's missing just to see if it's an API config error 
    # Or we can just let it run.
    res = provider.extract_text(image)
    print("Result:", res)
except Exception as e:
    import traceback
    traceback.print_exc()
