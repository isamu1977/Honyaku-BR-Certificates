import requests
from PIL import Image
import io

image = Image.new("RGB", (100, 100))
buf = io.BytesIO()
image.save(buf, format="JPEG")
buf.seek(0)

try:
    resp = requests.post("http://localhost:8000/upload", files={"file": ("test.jpg", buf, "image/jpeg")}, data={"provider": "mlx"})
    print(resp.status_code)
    print(resp.text)
except Exception as e:
    print(e)

