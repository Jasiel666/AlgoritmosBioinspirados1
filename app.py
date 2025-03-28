import streamlit as st
from models.genetics import genetic_algorithm
from models.immune_system import immune_algorithm_cancer
from models.aco_tsp import colonia_horm
from models.simulated_annealing import simulated_annealing

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
        simulated_annealing() 
    
    elif st.session_state.current_algorithm == "ant_colony":
        st.title("🐜 Algoritmo Colonia de Hormigas")
        colonia_horm()

    elif st.session_state.current_algorithm == "immune_system":
        st.title("🦠 Algoritmo de Sistemas Inmunes")
        immune_algorithm_cancer()
    
    if st.button("⬅️ Volver al Menú", key="back_to_menu"):
        change_page("menu")