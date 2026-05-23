import sys
import os
from pathlib import Path
import streamlit as st

# --- CORRECCIÓN DE RUTA DINÁMICA ---
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

# Imports
from services.vision_engine import VisionEngine
from services.viz_engine import VizEngine
from core.db import Database
from PIL import Image

# Configuración inicial (Debe ser el primer comando de streamlit)
st.set_page_config(page_title="OmniSolve AI", layout="wide")
db = Database()

def check_password():
    """Devuelve True si el usuario tiene permiso."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        # Aquí creamos el formulario de acceso
        st.title("🔒 Acceso Restringido")
        pwd = st.text_input("Introduce la contraseña para entrar:", type="password")
        if pwd == "gifiofovafanifi2609": # <--- CAMBIA ESTO por tu contraseña real
            st.session_state.password_correct = True
            st.rerun() 
        else:
            if pwd: # Solo muestra error si escribió algo y es incorrecto
                st.error("Contraseña incorrecta")
            st.stop() # Detiene la app aquí si la clave está mal o no se ha puesto

def main():
    # LLAMADA OBLIGATORIA AL INICIO
    check_password() 
    
    st.title("🎓 OmniSolve AI")
    
    # Creamos dos pestañas
    tab1, tab2 = st.tabs(["📸 Resolver con IA (Fotos)", "💬 Chat General"])

    # --- PESTAÑA 1: RESOLVER CON IA ---
    with tab1:
        archivo = st.file_uploader("Sube una foto de tu ejercicio", type=['png', 'jpg', 'jpeg'])

        if archivo:
            imagen = Image.open(archivo)
            st.image(imagen, caption="Imagen cargada", width=400)
            
            if st.button("Resolver con IA"):
                with st.spinner("OmniSolve está analizando..."):
                    try:
                        engine = VisionEngine()
                        data = engine.analizar_apunte(imagen, "Universidad")
                        
                        # Mostrar resultados
                        st.subheader(f"Área: {data.get('tipo', 'general').capitalize()}")
                        st.write(data.get('explicacion', 'No se pudo generar explicación.'))
                        st.success(f"**Resultado:** {data.get('resultado', 'N/A')}")
                        
                        # Lógica de graficación
                        if data.get("necesita_grafica") == True:
                            st.info(f"Detecté que requiere gráfica: {data.get('funcion_para_graficar')}")
                            fig = VizEngine.graficar_funcion(data.get('funcion_para_graficar'))
                            if fig:
                                st.plotly_chart(fig)
                            else:
                                st.warning("La IA sugirió gráfica pero no pude procesar la función.")

                        # Guardar historial
                        db.guardar_ejercicio(str(data.get('tipo')), str(data.get('resultado')))
                    except Exception as e:
                        st.error(f"Ocurrió un error al procesar: {e}")

    # --- PESTAÑA 2: CHAT GENERAL ---
    with tab2:
        st.subheader("Asistente General")
        
        # Inicializar el motor para el chat
        if "engine" not in st.session_state:
            st.session_state.engine = VisionEngine()
        
        # Inicializar historial si no existe
        if "mensajes" not in st.session_state:
            st.session_state.mensajes = []

        # Mostrar mensajes anteriores
        for msg in st.session_state.mensajes:
            with st.chat_message(msg["rol"]):
                st.write(msg["contenido"])

        # Si el usuario escribe
        if prompt := st.chat_input("Escribe cualquier pregunta aquí..."):
            # Guardar y mostrar mensaje del usuario
            st.session_state.mensajes.append({"rol": "user", "contenido": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            # Procesar
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    respuesta = st.session_state.engine.ask_text(prompt)
                    st.write(respuesta)
                # Guardar respuesta
                st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta})

if __name__ == "__main__":
    main()