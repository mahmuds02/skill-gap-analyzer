import os
from pathlib import Path

# Method 1: Check file exists
env_path = Path('.env')
print(f"📁 .env file exists: {env_path.exists()}")
print(f"📂 Current directory: {os.getcwd()}")

# Method 2: Try loading manually
if env_path.exists():
    print("\n📄 .env file contents:")
    with open('.env', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            print(f"  Line {i}: {repr(line)}")

# Method 3: Load with dotenv
from dotenv import load_dotenv
load_dotenv()

# Method 4: Get the value
api_key = os.getenv('GEMINI_API_KEY')
print(f"\n🔑 API key from os.getenv: {api_key}")

# Method 5: Load with explicit path
load_dotenv('.env', override=True)
api_key2 = os.getenv('GEMINI_API_KEY')
print(f"�� API key with explicit path: {api_key2}")
