import google.generativeai as genai
import json
import os
import streamlit as st

class VisionEngine:
    def __init__(self):
        # Clave hardcodeada para funcionamiento inmediato
        api_key = "AIzaSyCp4U9SMRY1JCI44AS-6kZ9TO3Dxzg0Ev4"
        genai.configure(api_key=api_key)
        
        # Configuramos el modelo una sola vez
        self.model = genai.GenerativeModel('models/gemini-3.5-flash')

    def analizar_apunte(self, imagen, nivel):
        prompt = f"""
        Eres un tutor experto en ingeniería, física, química y matemáticas. Analiza la imagen.
        Responde exclusivamente en formato JSON, sin texto previo ni posterior.
        Usa esta estructura exacta:
        {{
            "tipo": "ecuacion",
            "explicacion": "explicacion paso a paso",
            "resultado": "resultado final",
            "necesita_grafica": true,
            "funcion_para_graficar": "x**2"
        }}
        El usuario está en nivel: {nivel}.
        """
        
        try:
            # Enviamos la imagen y el prompt
            response = self.model.generate_content([prompt, imagen])
            
            # Limpieza básica del texto de respuesta
            texto = response.text.replace("```json", "").replace("```", "").strip()
            
            # Convertimos a diccionario
            return json.loads(texto)
            
        except Exception as e:
            # Si falla la IA, devolvemos un error estructurado para no romper la app
            return {
                "tipo": "error",
                "explicacion": f"Error al procesar: {str(e)}",
                "resultado": "No se pudo obtener respuesta.",
                "necesita_grafica": False,
                "funcion_para_graficar": None
            }

    def ask_text(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Ups, algo salió mal: {e}"