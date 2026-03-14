import requests

url = "http://localhost:8000/upload"
data = {"provider": "gemini"}

# Provide a dummy 1x1 image
empty_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa74B\x12\x00\x00\x00\x00IEND\xaeB`\x82'
files = {"file": ("test.png", empty_image, "image/png")}

response = requests.post(url, data=data, files=files)
print("Status Code:", response.status_code)
print("Response JSON:")
print(response.json())
