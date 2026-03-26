import requests
import json

base_url = "http://127.0.0.1:5000"

print("Testing reset-password endpoint directly")
payload = {
    "email": "test@example.com",
    "new_password": "newpassword123"
}
res = requests.post(f"{base_url}/reset-password", json=payload)
print("Response:", res.status_code, res.text)
