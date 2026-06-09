import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Ecuaciones Diferenciales", layout="wide")
st.title("📈 Solucionador y Graficador de Ecuaciones Diferenciales")
st.markdown("Resuelve analíticamente y grafica las EDOs propuestas.")

# Barra lateral para seleccionar ecuación y constantes
st.sidebar.header("⚙️ Configuración")
eq_option = st.sidebar.selectbox(
    "Selecciona la ecuación diferencial",
    [
        "1. dy/dx = 2x/(3y²)",
        "2. (x+1) dy/dx = x+6",
        "3. dy/dx = sen(4x)",
        "4. dy/dx + (1+y³)/(x y²(1+x²)) = 0"
    ]
)

# Rango de x para graficar
x_min = st.sidebar.slider("x mínimo", -5.0, 0.0, -3.0, 0.5)
x_max = st.sidebar.slider("x máximo", 0.0, 5.0, 3.0, 0.5)

# Definir función para graficar
def plot_solution(x, y, title, y_label):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, linewidth=2, color='royalblue')
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("x")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    return fig

# Caso 1: dy/dx = 2x/(3y²)  -> y³ = x² + C
if eq_option.startswith("1."):
    st.subheader("📐 Ecuación 1: $\\frac{dy}{dx} = \\frac{2x}{3y^2}$")
    st.latex(r"\frac{dy}{dx} = \frac{2x}{3y^2}")
    st.markdown("**Solución analítica:**")
    st.latex(r"y^3 = x^2 + C \quad\Rightarrow\quad y = \sqrt[3]{x^2 + C}")
    
    C = st.sidebar.slider("Constante C (y³ = x² + C)", -5.0, 5.0, 1.0, 0.2)
    x = np.linspace(x_min, x_max, 500)
    y = np.cbrt(x**2 + C)   # raíz cúbica real
    
    fig = plot_solution(x, y, f"Solución y = ∛(x² + {C:.2f})", "y")
    st.pyplot(fig)

# Caso 2: (x+1) dy/dx = x+6  -> y = x + 5 ln|x+1| + C
elif eq_option.startswith("2."):
    st.subheader("📐 Ecuación 2: $(x+1)\\frac{dy}{dx} = x+6$")
    st.latex(r"(x+1)\frac{dy}{dx} = x+6")
    st.markdown("**Solución analítica:**")
    st.latex(r"y = x + 5\ln|x+1| + C")
    
    C = st.sidebar.slider("Constante C", -5.0, 5.0, 1.0, 0.2)
    x = np.linspace(x_min, x_max, 500)
    # Evitar x = -1 (asíntota)
    x = x[x != -1.0]
    if len(x) == 0:
        st.error("El rango seleccionado contiene solo x = -1 (asíntota). Ajusta los límites.")
    else:
        y = x + 5 * np.log(np.abs(x + 1)) + C
        fig = plot_solution(x, y, f"y = x + 5 ln|x+1| + {C:.2f}", "y")
        st.pyplot(fig)

# Caso 3: dy/dx = sen(4x)  -> y = -1/4 cos(4x) + C
elif eq_option.startswith("3."):
    st.subheader("📐 Ecuación 3: $\\frac{dy}{dx} = \\sin(4x)$")
    st.latex(r"\frac{dy}{dx} = \sin(4x)")
    st.markdown("**Solución analítica:**")
    st.latex(r"y = -\frac{1}{4}\cos(4x) + C")
    
    C = st.sidebar.slider("Constante C", -5.0, 5.0, 1.0, 0.2)
    x = np.linspace(x_min, x_max, 500)
    y = -0.25 * np.cos(4*x) + C
    fig = plot_solution(x, y, f"y = -¼ cos(4x) + {C:.2f}", "y")
    st.pyplot(fig)

# Caso 4: dy/dx + (1+y³)/(x y²(1+x²)) = 0  -> 1+y³ = K*(1+x²)^(3/2)/x³
else:
    st.subheader("📐 Ecuación 4: $\\frac{dy}{dx} + \\frac{1+y^3}{x\\,y^2(1+x^2)} = 0$")
    st.latex(r"\frac{dy}{dx} + \frac{1+y^3}{x\,y^2(1+x^2)} = 0")
    st.markdown("**Solución analítica (implícita):**")
    st.latex(r"1 + y^3 = K\,\frac{(1+x^2)^{3/2}}{x^3}")
    st.markdown("Donde $K$ es una constante arbitraria.")
    
    K = st.sidebar.slider("Constante K (positiva)", 0.1, 5.0, 1.0, 0.1)
    # x no puede ser 0, y además necesitamos que el radicando sea positivo para la raíz cúbica real
    x_vals = np.linspace(x_min, x_max, 500)
    x_vals = x_vals[np.abs(x_vals) > 1e-6]  # eliminar x=0
    if len(x_vals) == 0:
        st.error("El rango seleccionado no contiene puntos válidos (x=0 excluido). Ajusta los límites.")
    else:
        # Calcular y a partir de la solución implícita: y = ( K*(1+x²)^(1.5)/x³ - 1 )^(1/3)
        # Nota: para evitar números complejos, forzamos que el interior sea >= 0
        interior = K * (1 + x_vals**2)**1.5 / x_vals**3 - 1
        # Solo graficar donde interior >= 0 (para raíz cúbica real, el radicando puede ser negativo,
        # pero la raíz cúbica real está definida para todo real, sin embargo aquí la expresión original
        # tiene sentido real si 1+y³ tiene el mismo signo que K... usamos np.cbrt para dominio real completo)
        y_vals = np.cbrt(interior)   # raíz cúbica real
        
        fig = plot_solution(x_vals, y_vals, f"Solución (K = {K:.2f})", "y")
        st.pyplot(fig)

# Información adicional
with st.expander("📘 Notas sobre las soluciones"):
    st.markdown("""
    - **Ecuación 1:** Separable, se integra directamente.
    - **Ecuación 2:** Lineal de primer orden, se resuelve por integración.
    - **Ecuación 3:** Integración directa.
    - **Ecuación 4:** Separable, requiere fracciones parciales y sustitución \(u = y^3\).
    - En todos los casos se ha omitido la constante de integración (o se incluye en el deslizador).
    - Los gráficos muestran la familia de curvas para un valor concreto de la constante.
    """)
