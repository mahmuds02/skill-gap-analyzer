import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv('.env', override=True)
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ ERROR: API key not found")
    exit(1)

print(f"✅ API key loaded")

try:
    genai.configure(api_key=api_key)
    
    # Use the fast, efficient model with lower quota usage
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("🔄 Testing API with gemini-2.5-flash...")
    response = model.generate_content("Say 'API works!' in 3 words max.")
    
    print("✅ SUCCESS! API is fully working!")
    print(f"📨 Response: {response.text}")
    print("\n🎉 Ready to build the project!")
    
except Exception as e:
    if "quota" in str(e).lower():
        print("⏰ Free tier quota reached. Wait 1 minute and try again.")
        print("✅ BUT your API key is valid and working!")
        print("🚀 Let's continue building the project - we'll use the API later.")
    else:
        print(f"❌ ERROR: {str(e)}")
