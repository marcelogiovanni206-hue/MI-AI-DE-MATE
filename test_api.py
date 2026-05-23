import google.generativeai as genai

# Pega aquí tu API KEY real entre las comillas
API_KEY = "AIzaSyCp4U9SMRY1JCI44AS-6kZ9TO3Dxzg0Ev4"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.0-pro')
    
    print("Conectando con Google...")
    response = model.generate_content("Hola, si recibes este mensaje, responde 'Conexión exitosa'.")
    
    print("\n--- RESULTADO ---")
    print(response.text)
    
except Exception as e:
    print(f"\n--- ERROR ---")
    print(f"Detalle del error: {e}")