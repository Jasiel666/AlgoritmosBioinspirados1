import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def hormigas_tsp(distancias, hormigas, iteraciones, tasa_evaporacion):
    n = len(distancias)
    mejor_camino, mejor_dist = None, np.inf
    progress_bar = st.progress(0)
    
    for it in range(iteraciones):
        for _ in range(hormigas):
            camino = list(np.random.permutation(n))
            dist = sum(distancias[camino[i]][camino[(i+1) % n]] for i in range(n))
            if dist < mejor_dist:
                mejor_camino, mejor_dist = camino, dist
        progress_bar.progress((it + 1) / iteraciones)
    
    return mejor_camino, mejor_dist

def colonia_horm():
    st.sidebar.markdown("### ⚙️ Parámetros del ACO")
    num_hormigas = st.sidebar.slider("Número de hormigas", 5, 100, 20)
    iteraciones = st.sidebar.slider("Iteraciones", 10, 500, 50)
    tasa_evaporacion = st.sidebar.slider("Tasa de evaporación", 0.1, 0.9, 0.5)
    
    ciudades = ["A", "B", "C", "D", "E"]
    distancias = np.array([
        [np.inf, 2, 5, 3, 7],
        [2, np.inf, 4, 1, 6],
        [5, 4, np.inf, 7, 3],
        [3, 1, 7, np.inf, 4],
        [7, 6, 3, 4, np.inf]
    ])
    
    st.subheader("📍 Matriz de Distancias")
    st.dataframe(pd.DataFrame(distancias, columns=ciudades, index=ciudades))
    
    if st.button("🚀 Ejecutar Algoritmo"):
        with st.spinner("Optimizando ruta..."):
            ruta_optima, distancia = hormigas_tsp(distancias, num_hormigas, iteraciones, tasa_evaporacion)
        
        st.success("¡Optimización completada!")
        st.metric("Distancia total", f"{distancia:.2f} unidades")
        st.metric("Ruta más corta", " → ".join([ciudades[i] for i in ruta_optima]))
        
        fig, ax = plt.subplots()
        coords = np.random.rand(len(ciudades), 2) * 10
        for i in range(len(ruta_optima)):
            inicio, fin = ruta_optima[i], ruta_optima[(i+1) % len(ruta_optima)]
            ax.plot([coords[inicio, 0], coords[fin, 0]], [coords[inicio, 1], coords[fin, 1]], 'b-')
        ax.scatter(coords[:, 0], coords[:, 1], c='red')
        for i, ciudad in enumerate(ciudades):
            ax.text(coords[i, 0], coords[i, 1], ciudad, fontsize=12)
        st.pyplot(fig)
