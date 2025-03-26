#C:\Users\k3nia\AppData\Local\Programs\Python\Python313\python.exe -m streamlit run app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Inicializar el estado de la página si no existe
if "page" not in st.session_state:
    st.session_state.page = "menu"

# Función para cambiar de página y recargar la interfaz
def change_page(page_name):
    st.session_state.page = page_name
    st.rerun()  # 🔄 Nuevo método para actualizar la interfaz

# Menú principal con botones
if st.session_state.page == "menu":
    st.title("Bienvenido a la Aplicación de Algoritmos")
    st.write("Selecciona un algoritmo para visualizar:")

    if st.button("Algoritmo Genético"):
        change_page("algoritmo1")

    if st.button("Algoritmo Recocido Simulado"):
        change_page("algoritmo2")

    if st.button("Algoritmo Colonia de Hormigas"):
        change_page("algoritmo3")

    if st.button("Algoritmo de Sistemas Inmunes"):
        change_page("algoritmo4")

# Página del Algoritmo Genético
elif st.session_state.page == "algoritmo1":
    st.title("Algoritmo Genético")
    st.write("Aquí puedes poner la implementación del Algoritmo Genético.")
    
    if st.button("Volver al Menú"):
        change_page("menu")

# Página del Algoritmo de Recocido Simulado
elif st.session_state.page == "algoritmo2":
    st.title("Algoritmo de Recocido Simulado")
    st.write("Aquí puedes poner la implementación del Algoritmo de Recocido Simulado.")
    
    if st.button("Volver al Menú"):
        change_page("menu")

# Página del Algoritmo de Colonia de Hormigas
elif st.session_state.page == "algoritmo3":
    st.title("Algoritmo de Colonia de Hormigas")
    
    # --- Configuración de parámetros ---
    st.sidebar.header("Parámetros del ACO")
    num_hormigas = st.sidebar.slider("Número de hormigas", 5, 100, 20)
    iteraciones = st.sidebar.slider("Iteraciones", 10, 500, 50)
    tasa_evaporacion = st.sidebar.slider("Tasa de evaporación", 0.1, 0.9, 0.5)
    
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
    if st.button("Ejecutar Algoritmo"):
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
            st.metric("Distancia total", f"{distancia:.2f} unidades")
        with col2:
            st.metric("Ruta más corta", " → ".join([ciudades[i] for i in ruta_optima]))
        
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
    
    # --- Botón para volver al menú ---
    if st.button("Volver al Menú"):
        st.session_state.page = "menu"  # O usar tu función change_page("menu")

# Página del Algoritmo de Sistemas Inmunes
elif st.session_state.page == "algoritmo4":
    st.title("Algoritmo de Sistemas Inmunes")
    st.write("Aquí puedes poner la implementación del Algoritmo de Sistemas Inmunes.")
    
    if st.button("Volver al Menú"):
        change_page("menu")
