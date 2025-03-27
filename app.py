# app.py
import streamlit as st
from models.genetics import genetic_algorithm
from models.immune_system import immune_algorithm_cancer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "current_algorithm" not in st.session_state:
    st.session_state.current_algorithm = None

# Function to change pages
def change_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Main menu
if st.session_state.page == "menu":
    st.title("Bienvenido a la Aplicación de Algoritmos")
    st.write("Selecciona un algoritmo para visualizar:")

    if st.button("Algoritmo Genético", key="btn_menu_genetic"):
        st.session_state.current_algorithm = "genetic"
        change_page("algorithm")

    if st.button("Algoritmo Recocido Simulado", key="btn_menu_simanneal"):
        st.session_state.current_algorithm = "simulated_annealing"
        change_page("algorithm")

    if st.button("Algoritmo Colonia de Hormigas", key="btn_menu_ants"):
        st.session_state.current_algorithm = "ant_colony"
        change_page("algorithm")

    if st.button("Algoritmo de Sistemas Inmunes", key="btn_menu_immune"):
        st.session_state.current_algorithm = "immune_system"
        change_page("algorithm")

# Unified algorithm page
elif st.session_state.page == "algorithm":
    if st.session_state.current_algorithm == "genetic":
        st.title("Algoritmo Genético")
        genetic_algorithm()
        
        if st.button("Volver al Menú", key="btn_back_genetic"):
            change_page("menu")

    elif st.session_state.current_algorithm == "simulated_annealing":
        st.title("Algoritmo Recocido Simulado")
        st.write("Aquí puedes poner la implementación del Algoritmo de Recocido Simulado.")
        
        if st.button("Volver al Menú", key="btn_back_simanneal"):
            change_page("menu")

    elif st.session_state.current_algorithm == "ant_colony":
        st.title("Algoritmo Colonia de Hormigas")
        
        # --- Configuración de parámetros ---
        st.sidebar.header("Parámetros del ACO")
        num_hormigas = st.sidebar.slider("Número de hormigas", 5, 100, 20, key="slider_ants")
        iteraciones = st.sidebar.slider("Iteraciones", 10, 500, 50, key="slider_iter")
        tasa_evaporacion = st.sidebar.slider("Tasa de evaporación", 0.1, 0.9, 0.5, key="slider_evap")
        
        # --- Matriz de distancias ---
        ciudades = ["A", "B", "C", "D", "E"]
        distancias = [
            [np.inf, 2, 5, 3, 7],
            [2, np.inf, 4, 1, 6],
            [5, 4, np.inf, 7, 3],
            [3, 1, 7, np.inf, 4],
            [7, 6, 3, 4, np.inf]
        ]
        
        st.subheader("Matriz de Distancias")
        st.write(pd.DataFrame(distancias, columns=ciudades, index=ciudades))
        
        # --- Algoritmo ---
        def hormigas_tsp(distancias, hormigas=20, iteraciones=50, tasa_evaporacion=0.5):
            n = len(distancias)
            feromonas = np.ones((n,n))
            mejor_camino, mejor_dist = None, np.inf
            
            progress_bar = st.progress(0)
            
            for it in range(iteraciones):
                for _ in range(hormigas):
                    camino = list(np.random.permutation(n))
                    dist = sum(distancias[camino[i]][camino[(i+1)%n]] for i in range(n))
                    if dist < mejor_dist:
                        mejor_camino, mejor_dist = camino, dist
                feromonas = feromonas * tasa_evaporacion + 1/(mejor_dist+1e-10)
                progress_bar.progress((it + 1) / iteraciones)
            
            return [int(ciudad) for ciudad in mejor_camino], mejor_dist
        
        # --- Botón de ejecución ---
        if st.button("Ejecutar Algoritmo", key="btn_run_ants"):
            with st.spinner('Optimizando ruta...'):
                ruta_optima, distancia = hormigas_tsp(
                    distancias, 
                    num_hormigas, 
                    iteraciones, 
                    tasa_evaporacion
                )
            
            # --- Resultados ---
            st.success("¡Optimización completada!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Distancia total", f"{distancia:.2f} unidades", key="metric_dist")
            with col2:
                st.metric("Ruta más corta", " → ".join([ciudades[i] for i in ruta_optima]), key="metric_route")
            
            # --- Gráfico ---
            fig, ax = plt.subplots()
            coords = np.random.rand(len(ciudades), 2) * 10
            for i in range(len(ruta_optima)):
                inicio, fin = ruta_optima[i], ruta_optima[(i+1)%len(ruta_optima)]
                ax.plot([coords[inicio,0], coords[fin,0]], [coords[inicio,1], coords[fin,1]], 'b-')
            ax.scatter(coords[:,0], coords[:,1], c='red')
            for i, ciudad in enumerate(ciudades):
                ax.text(coords[i,0], coords[i,1], ciudad, fontsize=12)
            st.pyplot(fig)
        
        if st.button("Volver al Menú", key="btn_back_ants"):
            change_page("menu")

    elif st.session_state.current_algorithm == "immune_system":
        st.title("Algoritmo de Sistemas Inmunes")
        immune_algorithm_cancer()
        
        if st.button("Volver al Menú", key="btn_back_immune"):
            change_page("menu")