import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import MinMaxScaler

def immune_algorithm_cancer():
    # Cargar dataset de cáncer de mama (Wisconsin)
    cancer_data = load_breast_cancer()
    X = cancer_data.data
    y = cancer_data.target
    features = cancer_data.feature_names
    
    # Normalizar datos
    scaler = MinMaxScaler()
    X_normalized = scaler.fit_transform(X)
    
    # Dividir en patrones benignos (0) y malignos (1)
    benign_patterns = X_normalized[y == 0]
    malignant_patterns = X_normalized[y == 1]
    
    st.sidebar.header("⚙️ Parámetros del AIS Oncológico")
    population_size = st.sidebar.slider("Tamaño de población de linfocitos", 50, 500, 100)
    generations = st.sidebar.slider("Generaciones de evolución", 10, 200, 50)
    mutation_rate = st.sidebar.slider("Tasa de mutación", 0.01, 0.3, 0.05)
    detection_threshold = st.sidebar.slider("Umbral de detección", 0.5, 0.99, 0.85)
    
    # Visualización de datos
    st.subheader("🔬 Dataset de Cáncer de Mama")
    st.write(f"**{len(benign_patterns)} patrones benignos** | **{len(malignant_patterns)} patrones malignos**")
    st.write("Características seleccionadas:")
    selected_features = features[::5]  # Mostrar cada 5 features por espacio
    st.write(", ".join(selected_features))
    
    # Generar población inicial de detectores (linfocitos T virtuales)
    def generate_detectors(size):
        return np.random.uniform(low=0, high=1, size=(size, X.shape[1]))
    
    # Función de reconocimiento (similitud coseno)
    def recognize(detector, pattern):
        return np.dot(detector, pattern) / (np.linalg.norm(detector) * np.linalg.norm(pattern))
    
    # Algoritmo principal
    def train_ais():
        detectors = generate_detectors(population_size)
        detection_history = []
        false_positives_history = []
        
        progress_bar = st.progress(0)
        fig_placeholder = st.empty()
        
        for gen in range(generations):
            true_detections = 0
            false_positives = 0
            
            # Evaluar contra patrones malignos (cancerosos)
            for pattern in malignant_patterns:
                for detector in detectors:
                    if recognize(detector, pattern) > detection_threshold:
                        true_detections += 1
                        break
            
            # Evaluar contra patrones benignos (para falsos positivos)
            for pattern in benign_patterns:
                for detector in detectors:
                    if recognize(detector, pattern) > detection_threshold:
                        false_positives += 1
                        break
            
            # Calcular métricas
            detection_rate = true_detections / len(malignant_patterns)
            fp_rate = false_positives / len(benign_patterns)
            detection_history.append(detection_rate)
            false_positives_history.append(fp_rate)
            
            # Selección clonal (los mejores detectores se replican)
            detector_performance = [
                np.mean([recognize(d, p) for p in malignant_patterns])
                for d in detectors
            ]
            best_indices = np.argsort(detector_performance)[-int(population_size*0.2):]
            clones = np.array([mutate(detectors[i], mutation_rate) 
                             for i in best_indices
                             for _ in range(5)])  # Cada uno genera 5 clones
            
            # Reemplazar peores detectores
            detectors = np.vstack([
                detectors[best_indices],
                clones,
                generate_detectors(int(population_size*0.3))
            ])
            
            # Actualizar visualización
            if gen % 5 == 0 or gen == generations - 1:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(detection_history, 'g-', label="Detección de malignos")
                ax.plot(false_positives_history, 'r--', label="Falsos positivos")
                ax.set_title("Evolución del Sistema Inmune Artificial")
                ax.set_xlabel("Generación")
                ax.set_ylabel("Tasa")
                ax.legend()
                ax.grid(True)
                fig_placeholder.pyplot(fig)
                plt.close()
            
            progress_bar.progress((gen + 1) / generations)
        
        return detectors, detection_history[-1], false_positives_history[-1]
    
    # Función de mutación
    def mutate(detector, rate):
        mask = np.random.rand(len(detector)) < rate
        noise = np.random.normal(0, 0.1, len(detector))
        return np.clip(detector + mask * noise, 0, 1)
    
    # Interfaz principal
    if st.button("🚀 Entrenar Sistema Inmune Artificial"):
        st.info("Entrenando detectores para cáncer...")
        
        final_detectors, detection_rate, fp_rate = train_ais()
        
        st.success("¡Entrenamiento completado!")
        col1, col2 = st.columns(2)
        col1.metric("Tasa de detección de malignos", f"{detection_rate*100:.2f}%")
        col2.metric("Tasa de falsos positivos", f"{fp_rate*100:.2f}%")
        
        # Mostrar características más importantes
        st.subheader("🔍 Detectores Óptimos")
        mean_detector = np.mean(final_detectors, axis=0)
        top_features_idx = np.argsort(mean_detector)[-5:][::-1]
        
        st.write("Características más relevantes identificadas:")
        for idx in top_features_idx:
            st.write(f"- **{features[idx]}**: {mean_detector[idx]:.3f}")
        
        # Visualización 2D (PCA simplificado)
        st.subheader("🧫 Visualización de Patrones")
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_normalized)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(X_pca[y==0, 0], X_pca[y==0, 1], c='green', alpha=0.6, label='Benigno')
        ax.scatter(X_pca[y==1, 0], X_pca[y==1, 1], c='red', alpha=0.6, label='Maligno')
        
        # Proyectar algunos detectores
        detector_pca = pca.transform(final_detectors[:20])
        ax.scatter(detector_pca[:, 0], detector_pca[:, 1], c='blue', marker='x', 
                  s=100, linewidths=2, label='Detectores AIS')
        
        ax.set_title("Espacio de características (PCA reducido)")
        ax.legend()
        st.pyplot(fig)