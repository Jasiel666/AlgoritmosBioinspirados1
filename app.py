import streamlit as st

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
   # Página del Algoritmo de Colonia de Hormigas
elif st.session_state.page == "algoritmo3":
    st.title("Algoritmo de Colonia de Hormigas (ACO)")
    st.write("Implementación del algoritmo para resolver el Problema del Viajante (TSP)")
    
    # Configuración de parámetros en el sidebar
    st.sidebar.header("Parámetros del ACO")
    num_hormigas = st.sidebar.slider("Número de hormigas", 5, 100, 20)
    iteraciones = st.sidebar.slider("Iteraciones", 10, 500, 50)
    tasa_evaporacion = st.sidebar.slider("Tasa de evaporación", 0.1, 0.9, 0.5)
    
    # Matriz de distancias - el usuario puede cargar o usar ejemplo
    st.subheader("Matriz de Distancias")
    opcion_matriz = st.radio("Seleccione opción:", 
                            ("Usar ejemplo predefinido", "Cargar matriz personalizada"))
    
    if opcion_matriz == "Usar ejemplo predefinido":
        distancias = [
            [np.inf, 2, 5, 3, 7],
            [2, np.inf, 4, 1, 6],
            [5, 4, np.inf, 7, 3],
            [3, 1, 7, np.inf, 4],
            [7, 6, 3, 4, np.inf]
        ]
        ciudades = ["A", "B", "C", "D", "E"]
    else:
        # Aquí podrías implementar la carga de una matriz personalizada
        st.warning("Implementar carga de matriz personalizada aquí")
        distancias = []
        ciudades = []
    
    # Mostrar matriz de distancias
    st.write("Matriz de distancias actual:")
    st.write(pd.DataFrame(distancias, columns=ciudades, index=ciudades))
    
    # Ejecutar algoritmo cuando se presiona el botón
    if st.button("Ejecutar Algoritmo"):
        with st.spinner('Optimizando ruta con colonia de hormigas...'):
            # Función modificada para usar los parámetros de la interfaz
            def hormigas_tsp(distancias, hormigas=num_hormigas, iteraciones=iteraciones):
                n = len(distancias)
                feromonas = np.ones((n,n))
                mejor_camino, mejor_dist = None, np.inf
                
                # Barra de progreso
                progress_bar = st.progress(0)
                
                for it in range(iteraciones):
                    for _ in range(hormigas):
                        camino = list(np.random.permutation(n))
                        dist = sum(distancias[camino[i]][camino[(i+1)%n]] for i in range(n))
                        if dist < mejor_dist:
                            mejor_camino, mejor_dist = camino, dist
                    feromonas = feromonas * tasa_evaporacion + 1/(mejor_dist+1e-10)
                    progress_bar.progress((it + 1) / iteraciones)
                
                camino_limpio = [int(ciudad) for ciudad in mejor_camino]
                return camino_limpio, mejor_dist
            
            ruta_optima, distancia = hormigas_tsp(distancias)
            
            # Mostrar resultados
            st.success("¡Optimización completada!")
            st.subheader("Resultados")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Distancia total óptima", f"{distancia:.2f} unidades")
            
            with col2:
                st.metric("Número de ciudades", len(ruta_optima))
            
            # Visualización de la ruta
            st.subheader("Ruta óptima encontrada")
            ruta_nombres = " → ".join([ciudades[i] for i in ruta_optima] + [ciudades[ruta_optima[0]]])
            st.write(f"🔹 {ruta_nombres}")
            
            # Detalle del recorrido
            st.subheader("Detalle del recorrido")
            detalle = ""
            for i in range(len(ruta_optima)):
                ciudad_actual = ruta_optima[i]
                ciudad_siguiente = ruta_optima[(i+1)%len(ruta_optima)]
                detalle += f"{ciudades[ciudad_actual]} → {ciudades[ciudad_siguiente]}: {distancias[ciudad_actual][ciudad_siguiente]} unidades\n"
            
            st.text_area("Distancia entre ciudades:", detalle, height=150)
            
            # Gráfico simple de la ruta (opcional)
            try:
                import matplotlib.pyplot as plt
                
                # Generar coordenadas aleatorias para visualización
                np.random.seed(42)
                coords = np.random.rand(len(ciudades), 2) * 10
                
                fig, ax = plt.subplots()
                # Dibujar las conexiones
                for i in range(len(ruta_optima)):
                    inicio = ruta_optima[i]
                    fin = ruta_optima[(i+1)%len(ruta_optima)]
                    ax.plot([coords[inicio,0], coords[fin,0]], 
                            [coords[inicio,1], coords[fin,1]], 'b-')
                
                # Dibujar los puntos
                ax.scatter(coords[:,0], coords[:,1], c='red')
                for i, ciudad in enumerate(ciudades):
                    ax.text(coords[i,0], coords[i,1], ciudad, fontsize=12)
                
                ax.set_title("Visualización de la Ruta Óptima")
                st.pyplot(fig)
            except:
                st.warning("No se pudo generar el gráfico. Asegúrate de tener matplotlib instalado.")
    
    if st.button("Volver al Menú"):
        change_page("menu")

# Página del Algoritmo de Sistemas Inmunes
elif st.session_state.page == "algoritmo4":
    st.title("Algoritmo de Sistemas Inmunes")
    st.write("Aquí puedes poner la implementación del Algoritmo de Sistemas Inmunes.")
    
    if st.button("Volver al Menú"):
        change_page("menu")
