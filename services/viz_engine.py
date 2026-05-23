import streamlit as st
import plotly.express as px
import numpy as np
import sympy as sp

class VizEngine:
    @staticmethod
    def graficar_funcion(ecuacion_str):
        try:
            x = sp.symbols('x')
            # Convertimos el string a expresión matemática
            expr = sp.sympify(ecuacion_str)
            f = sp.lambdify(x, expr, 'numpy')
            
            # Generamos puntos
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)
            
            # Creamos la gráfica con Plotly
            fig = px.line(x=x_vals, y=y_vals, title=f"Gráfica de {ecuacion_str}")
            return fig
        except Exception as e:
            st.error(f"Error al graficar: {e}")
            return None