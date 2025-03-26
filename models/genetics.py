import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Configuración de la página
st.set_page_config(page_title="Algoritmo Genético Interactivo", layout="wide")
st.title("🦠 Algoritmo Genético - Optimización de Funciones")

# Función de aptitud mejorada
def fitness_function(x):
    return np.sin(3 * x) + np.cos(5 * x) + 2

# Versión mejorada del algoritmo genético
def improved_genetic_algorithm():
    # Sidebar para controles interactivos
    with st.sidebar:
        st.header("⚙️ Parámetros del Algoritmo")
        num_generations = st.slider("Número de generaciones", 10, 100, 30)
        population_size = st.slider("Tamaño de la población", 10, 100, 20)
        mutation_rate = st.slider("Tasa de mutación", 0.01, 0.5, 0.1)
        crossover_rate = st.slider("Tasa de cruce", 0.1, 1.0, 0.7)
        speed = st.slider("Velocidad de animación", 0.1, 2.0, 0.5)
        
        st.markdown("---")
        st.markdown("**Cómo funciona:**")
        st.markdown("1. � Población inicial aleatoria")
        st.markdown("2. 🏆 Selección por torneo")
        st.markdown("3. 💑 Cruce de individuos")
        st.markdown("4. � Mutación aleatoria")
        st.markdown("5. 🔄 Repetir hasta convergencia")

    # Rango de visualización
    x_range = np.linspace(0, 2 * np.pi, 200)
    y_range = fitness_function(x_range)
    
    # Configuración de la figura
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.style.use('seaborn-darkgrid')
    
    # Línea de la función objetivo
    ax.plot(x_range, y_range, 'b-', linewidth=2, label="Función objetivo")
    
    # Límites del gráfico
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(min(y_range) - 0.5, max(y_range) + 0.5)
    ax.set_xlabel("Valor de x")
    ax.set_ylabel("Fitness")
    ax.set_title("Evolución de la Población")
    
    # Elementos visuales
    best_point, = ax.plot([], [], 'go', markersize=10, label="Mejor individuo")
    population_scatter = ax.scatter([], [], c='red', s=50, alpha=0.7, label="Población")
    ax.legend(loc="upper right")
    
    # Contenedor para la animación
    animation_placeholder = st.empty()
    
    # Generar población inicial
    population = np.random.uniform(0, 2 * np.pi, population_size)
    fitness_values = fitness_function(population)
    
    # Historial para estadísticas
    best_fitness_history = []
    avg_fitness_history = []
    
    # Progreso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Animación por generaciones
    for generation in range(num_generations):
        # Evaluar fitness
        fitness_values = fitness_function(population)
        
        # Selección por torneo (mejorada)
        selected_indices = []
        for _ in range(population_size):
            contestants = np.random.choice(range(population_size), size=3)
            winner = contestants[np.argmax(fitness_values[contestants])]
            selected_indices.append(winner)
        population = population[selected_indices]
        
        # Cruce (recombinación uniforme)
        children = []
        for i in range(0, population_size - 1, 2):
            if np.random.rand() < crossover_rate:
                alpha = np.random.rand()
                child1 = alpha * population[i] + (1 - alpha) * population[i+1]
                child2 = (1 - alpha) * population[i] + alpha * population[i+1]
                children.extend([child1, child2])
            else:
                children.extend([population[i], population[i+1]])
        population = np.array(children)
        
        # Mutación (no uniforme)
        for i in range(population_size):
            if np.random.rand() < mutation_rate:
                population[i] += np.random.normal(0, 0.5)
        
        # Mantener dentro de los límites
        population = np.clip(population, 0, 2 * np.pi)
        
        # Estadísticas
        current_best = np.max(fitness_values)
        best_fitness_history.append(current_best)
        avg_fitness_history.append(np.mean(fitness_values))
        
        # Actualizar visualización
        population_scatter.set_offsets(np.c_[population, fitness_function(population)])
        best_idx = np.argmax(fitness_values)
        best_point.set_data([population[best_idx]], [fitness_values[best_idx]])
        
        # Mostrar la figura actualizada
        animation_placeholder.pyplot(fig)
        
        # Actualizar progreso
        progress = (generation + 1) / num_generations
        progress_bar.progress(progress)
        status_text.text(f"Generación {generation + 1}/{num_generations} | Mejor fitness: {current_best:.4f}")
        
        # Pequeña pausa para la animación
        time.sleep(0.5 / speed)
    
    # Mostrar resultados finales
    st.success("¡Evolución completada! 🎉")
    
    # Gráfico de convergencia
    st.subheader("📈 Convergencia del Algoritmo")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(best_fitness_history, 'r-', label="Mejor fitness")
    ax2.plot(avg_fitness_history, 'b--', label="Fitness promedio")
    ax2.set_xlabel("Generación")
    ax2.set_ylabel("Fitness")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
    
    # Estadísticas finales
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mejor fitness encontrado", f"{max(best_fitness_history):.4f}")
    with col2:
        st.metric("Mejor solución encontrada", f"{population[np.argmax(fitness_values)]:.4f}")

# Ejecutar el algoritmo mejorado
if __name__ == "__main__":
    improved_genetic_algorithm()