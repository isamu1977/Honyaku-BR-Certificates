import sys
import traceback
sys.path.append('backend')
from services.ai_providers import LocalMLXProvider
from PIL import Image

provider = LocalMLXProvider()
img = Image.new("RGB", (10, 10))
res = provider.extract_text(img)
print("Result:", res)
