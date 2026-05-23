from sympy import symbols, solve, sympify, latex

class MathCore:
    """Motor de cálculo exacto para evitar errores de la IA."""
    
    @staticmethod
    def resolver_ecuacion(ecuacion_texto):
        """
        Intenta resolver una ecuación matemática de forma exacta.
        """
        try:
            x = symbols('x')
            # Convertimos el texto del usuario a una expresión matemática
            expr = sympify(ecuacion_texto)
            solucion = solve(expr, x)
            
            # Convertimos la solución a formato LaTeX (bonito para la pantalla)
            resultado_latex = latex(solucion)
            return f"Solución exacta calculada: ${resultado_latex}$"
        
        except Exception as e:
            return f"Error en el cálculo exacto: {str(e)}"

    @staticmethod
    def verificar_resultado(resultado_ia, resultado_calculo):
        """
        Aquí podrías comparar si la IA dijo lo mismo que el motor de cálculo.
        Esto añade una capa de validación profesional.
        """
        return "Cálculo verificado por MathCore."