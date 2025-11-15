"""
Test which Gemini models are available
"""
import google.generativeai as genai
from app.config import settings

# Configure API
genai.configure(api_key=settings.GEMINI_API_KEY)

print("🔍 Listing available Gemini models...")
print("=" * 60)

try:
    # List all models
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:100]}...")
            print()
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print()
    print("Let's try using models directly...")

    # Try different model names
    test_models = [
        'gemini-pro',
        'gemini-1.5-pro',
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest',
        'gemini-1.0-pro',
        'models/gemini-pro',
        'models/gemini-1.5-pro',
        'models/gemini-1.5-flash',
    ]

    for model_name in test_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Arr!' like a pirate")
            print(f"✅ {model_name} works! Response: {response.text[:50]}")
        except Exception as e:
            print(f"❌ {model_name} failed: {str(e)[:80]}")
