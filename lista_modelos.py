import google.generativeai as genai

# Pega aquí tu API KEY
API_KEY = "AIzaSyCp4U9SMRY1JCI44AS-6kZ9TO3Dxzg0Ev4"

genai.configure(api_key=API_KEY)

print("Buscando modelos disponibles...\n")

# Esto listará solo los modelos que pueden "generar contenido"
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Modelo encontrado: {m.name}")