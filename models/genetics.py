# models/genetics.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

def genetic_algorithm():
    # Initialize parameters in session state if they don't exist
    if 'ga_params' not in st.session_state:
        st.session_state.ga_params = {
            'num_generations': 30,
            'population_size': 20,
            'mutation_rate': 0.1,
            'crossover_rate': 0.7,
            'speed': 0.5
        }
    
    # Update parameters from sidebar
    with st.sidebar:
        st.session_state.ga_params['num_generations'] = st.slider(
            "Número de generaciones", 10, 100, 
            st.session_state.ga_params['num_generations'])
        st.session_state.ga_params['population_size'] = st.slider(
            "Tamaño de la población", 10, 100, 
            st.session_state.ga_params['population_size'])
        st.session_state.ga_params['mutation_rate'] = st.slider(
            "Tasa de mutación", 0.01, 0.5, 
            st.session_state.ga_params['mutation_rate'])
        st.session_state.ga_params['crossover_rate'] = st.slider(
            "Tasa de cruce", 0.1, 1.0, 
            st.session_state.ga_params['crossover_rate'])
        st.session_state.ga_params['speed'] = st.slider(
            "Velocidad de animación", 0.1, 2.0, 
            st.session_state.ga_params['speed'])
    
    # Extract parameters
    params = st.session_state.ga_params
    num_generations = params['num_generations']
    population_size = params['population_size']
    mutation_rate = params['mutation_rate']
    crossover_rate = params['crossover_rate']
    speed = params['speed']
    
    # Fitness function
    def fitness_function(x):
        return np.sin(3 * x) + np.cos(5 * x) + 2
    
    # Initialize population if not exists
    if 'ga_population' not in st.session_state:
        st.session_state.ga_population = np.random.uniform(0, 2 * np.pi, population_size)
        st.session_state.ga_fitness_history = []
        st.session_state.ga_avg_history = []
    
    # Get current state
    population = st.session_state.ga_population
    best_fitness_history = st.session_state.ga_fitness_history
    avg_fitness_history = st.session_state.ga_avg_history
    
    # Visualization setup
    x_range = np.linspace(0, 2 * np.pi, 200)
    y_range = fitness_function(x_range)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_style("darkgrid")
    ax.plot(x_range, y_range, 'b-', linewidth=2, label="Función objetivo")
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(min(y_range) - 0.5, max(y_range) + 0.5)
    ax.set_xlabel("Valor de x")
    ax.set_ylabel("Fitness")
    ax.set_title("Evolución de la Población")
    
    best_point, = ax.plot([], [], 'go', markersize=10, label="Mejor individuo")
    population_scatter = ax.scatter([], [], c='red', s=50, alpha=0.7, label="Población")
    ax.legend(loc="upper right")
    
    animation_placeholder = st.empty()
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Run button
    if st.button("Ejecutar Algoritmo Genético"):
        for generation in range(num_generations):
            # Evaluate fitness
            fitness_values = fitness_function(population)
            
            # Tournament selection
            selected_indices = []
            for _ in range(population_size):
                contestants = np.random.choice(range(population_size), size=3)
                winner = contestants[np.argmax(fitness_values[contestants])]
                selected_indices.append(winner)
            population = population[selected_indices]
            
            # Crossover
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
            
            # Mutation
            for i in range(population_size):
                if np.random.rand() < mutation_rate:
                    population[i] += np.random.normal(0, 0.5)
            
            # Keep within bounds
            population = np.clip(population, 0, 2 * np.pi)
            
            # Update state
            st.session_state.ga_population = population
            current_best = np.max(fitness_values)
            best_fitness_history.append(current_best)
            avg_fitness_history.append(np.mean(fitness_values))
            
            # Update visualization
            population_scatter.set_offsets(np.c_[population, fitness_function(population)])
            best_idx = np.argmax(fitness_values)
            best_point.set_data([population[best_idx]], [fitness_values[best_idx]])
            
            # Show updated figure
            animation_placeholder.pyplot(fig)
            
            # Update progress
            progress = (generation + 1) / num_generations
            progress_bar.progress(progress)
            status_text.text(f"Generación {generation + 1}/{num_generations} | Mejor fitness: {current_best:.4f}")
            
            time.sleep(0.5 / speed)
        
        # Show final results
        st.success("¡Evolución completada! 🎉")
        
        # Convergence plot
        st.subheader("📈 Convergencia del Algoritmo")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(best_fitness_history, 'r-', label="Mejor fitness")
        ax2.plot(avg_fitness_history, 'b--', label="Fitness promedio")
        ax2.set_xlabel("Generación")
        ax2.set_ylabel("Fitness")
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)
        
        # Final statistics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Mejor fitness encontrado", f"{max(best_fitness_history):.4f}")
        with col2:
            st.metric("Mejor solución encontrada", f"{population[np.argmax(fitness_values)]:.4f}")