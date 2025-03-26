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
    st.write("Aquí puedes poner la implementación del Algoritmo de Colonia de Hormigas.")
    
    if st.button("Volver al Menú"):
        change_page("menu")

# Página del Algoritmo de Sistemas Inmunes
elif st.session_state.page == "algoritmo4":
    st.title("Algoritmo de Sistemas Inmunes")
    st.write("Aquí puedes poner la implementación del Algoritmo de Sistemas Inmunes.")
    
    if st.button("Volver al Menú"):
        change_page("menu")
