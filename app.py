import streamlit as st
from models.genetics import genetic_algorithm
from models.immune_system import immune_algorithm_cancer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Custom styling for buttons
st.markdown("""
    <style>
        /* Button with linear gradient */
        div.stButton > button {
            background: linear-gradient(90deg, #ff5733, #c70039);
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 16px;
            transition: color 0.3s ease-in-out;
            border: none;
            cursor: pointer;
        }

        /* Change only text color on hover */
        div.stButton > button:hover {
            color: #ffff99 !important; /* Light Yellow */
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "current_algorithm" not in st.session_state:
    st.session_state.current_algorithm = None

def change_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Main menu
if st.session_state.page == "menu":
    st.title("🚀 Bienvenido a la Aplicación de Algoritmos")
    st.write("Selecciona un algoritmo para visualizar:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧬 Algoritmo Genético"):
            st.session_state.current_algorithm = "genetic"
            change_page("algorithm")
    with col2:
        if st.button("🔥 Algoritmo Recocido Simulado"):
            st.session_state.current_algorithm = "simulated_annealing"
            change_page("algorithm")
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🐜 Algoritmo Colonia de Hormigas"):
            st.session_state.current_algorithm = "ant_colony"
            change_page("algorithm")
    with col4:
        if st.button("🦠 Algoritmo de Sistemas Inmunes"):
            st.session_state.current_algorithm = "immune_system"
            change_page("algorithm")

# Algorithm page
elif st.session_state.page == "algorithm":
    st.sidebar.markdown("## 🔍 Opciones del Algoritmo")
    if st.sidebar.button("⬅️ Volver al Menú"):
        change_page("menu")
    
    if st.session_state.current_algorithm == "genetic":
        st.title("🧬 Algoritmo Genético")
        genetic_algorithm()
    
    elif st.session_state.current_algorithm == "simulated_annealing":
        st.title("🔥 Algoritmo Recocido Simulado")
        st.write("Aquí puedes poner la implementación del Algoritmo de Recocido Simulado.")
    
    elif st.session_state.current_algorithm == "ant_colony":
        st.title("🐜 Algoritmo Colonia de Hormigas")
        
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
        
        def hormigas_tsp(distancias, hormigas, iteraciones, tasa_evaporacion):
            n = len(distancias)
            mejor_camino, mejor_dist = None, np.inf
            progress_bar = st.progress(0)
            
            for it in range(iteraciones):
                for _ in range(hormigas):
                    camino = list(np.random.permutation(n))
                    dist = sum(distancias[camino[i]][camino[(i+1)%n]] for i in range(n))
                    if dist < mejor_dist:
                        mejor_camino, mejor_dist = camino, dist
                progress_bar.progress((it + 1) / iteraciones)
            
            return mejor_camino, mejor_dist
        
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

    elif st.session_state.current_algorithm == "immune_system":
        st.title("🦠 Algoritmo de Sistemas Inmunes")
        immune_algorithm_cancer()
    
    if st.button("⬅️ Volver al Menú", key="back_to_menu"):
        change_page("menu")