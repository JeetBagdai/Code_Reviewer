import sys
import os

if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

import json
import urllib.request
import urllib.error

API_URL = "https://api.groq.com/openai/v1/chat/completions"
KEY = os.environ.get("GROQ_API_KEY", "").strip()

print(f"Key loaded: {KEY[:8]}...{KEY[-4:]} Length: {len(KEY)}")

payload = json.dumps({
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "hello"}]
}).encode("utf-8")

req = urllib.request.Request(API_URL, data=payload, headers={
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

try:
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code)
    print("Body:", e.read().decode("utf-8"))
except Exception as e:
    print("Error:", e)

