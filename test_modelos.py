import os
from dotenv import load_dotenv
from google import genai

load_dotenv('.env')

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise RuntimeError('Falta GOOGLE_API_KEY en .env')

client = genai.Client(api_key=api_key)

print('Modelos con generateContent disponibles para esta API key:\n')
for model in client.models.list():
    methods = getattr(model, 'supported_actions', None) or getattr(model, 'supported_generation_methods', None) or []
    methods_text = ' '.join(methods) if isinstance(methods, list) else str(methods)
    if 'generateContent' in methods_text or 'generate_content' in methods_text:
        print(f"- {model.name.replace('models/', '')}")
