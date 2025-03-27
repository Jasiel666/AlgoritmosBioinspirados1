import numpy as np
import matplotlib.pyplot as plt
import random
import math

def simulated_annealing():
    """Función principal del algoritmo"""
    import streamlit as st
    
   
    with st.sidebar:
        st.header("⚙️ Parámetros del Recocido")
        temp = st.slider("Temperatura inicial", 100, 5000, 1000)
        enfriar = st.slider("Tasa de enfriamiento", 0.85, 0.99, 0.95)
        iteraciones = st.slider("Iteraciones", 10, 200, 100)
    
    
    def f(x): 
        return (x-3)**2 + 2*np.sin(x*2)
    
    
    x, historial = 10, []
    for _ in range(iteraciones):
        x_new = x + random.uniform(-2, 2)
        delta = f(x_new) - f(x)
        if delta < 0 or random.random() < math.exp(-delta/temp):
            x = x_new
        temp *= enfriar
        historial.append(f(x))
    
    
    col1, col2 = st.columns(2)
    col1.metric("Mejor solución", f"x = {x:.4f}")
    col2.metric("Valor mínimo", f"{f(x):.4f}")
    
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    x_vals = np.linspace(-2, 8, 100)
    
    ax1.plot(x_vals, [f(v) for v in x_vals], 'b-', label='Función')
    ax1.plot(x, f(x), 'ro', markersize=8, label='Mínimo')
    ax1.set_title("Función objetivo")
    ax1.legend()
    
    ax2.plot(historial, 'r-', linewidth=1.5)
    ax2.set_title("Convergencia del algoritmo")
    ax2.set_xlabel("Iteración")
    
    st.pyplot(fig)