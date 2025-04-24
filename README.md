# Detector de Emociones con IA

Este proyecto implementa un detector de emociones en tiempo real utilizando visión por computadora e inteligencia artificial. Mediante la cámara web, el sistema captura el rostro del usuario, procesa la imagen y determina el estado emocional, ofreciendo recomendaciones personalizadas basadas en las emociones detectadas.

## Características principales

- **Detección facial** en tiempo real mediante OpenCV
- **Reconocimiento de 7 emociones**: Feliz, Triste, Enojado, Temeroso, Disgustado, Sorprendido y Neutral
- **Interfaz gráfica intuitiva** con visualización del estado emocional
- **Sistema de recomendaciones** basadas en el estado emocional detectado:
  - Mensajes motivacionales
  - Sugerencias de música
  - Recomendaciones de acciones
  - Adaptación de colores según la emoción
- **Seguimiento de historial emocional** para análisis personal
- **Aplicación multi-hilo** para un rendimiento óptimo

## Requisitos

- Python 3.6+
- OpenCV
- TensorFlow 2.x
- NumPy
- Tkinter (incluido en la mayoría de las instalaciones de Python)

## Instalación

1. Clone este repositorio:
   ```
   git clone https://github.com/tu-usuario/detector-emociones.git
   cd detector-emociones
   ```

2. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Descargue el modelo pre-entrenado:
   El archivo `modelo_final.keras` debe estar en el directorio principal del proyecto.

## Uso

1. Ejecute el script principal:
   ```
   python app.py
   ```

2. Configure las preferencias de recomendaciones en la ventana de inicio.

3. Posicione su rostro frente a la cámara y mantenga una posición estable.

4. Después de unos segundos, el sistema detectará su emoción y mostrará recomendaciones personalizadas.

5. Utilice los controles:
   - **Q**: Salir de la aplicación
   - **R**: Reiniciar la detección
   - **M**: Reproducir música recomendada (cuando esté disponible)

## Estructura del proyecto

- `app.py`: Punto de entrada principal, configuración de la aplicación
- `detector.py`: Clase principal del detector de emociones
- `model_manager.py`: Gestiona el modelo de IA y las predicciones
- `ui_manager.py`: Gestiona la interfaz de usuario
- `recommendation_manager.py`: Sistema de recomendaciones personalizadas
- `entrenar_modelo.py`: Script para entrenar el modelo con el dataset RAF-DB
- `emotion_history.json`: Historial de emociones detectadas

## Modelo de IA

El modelo está entrenado con el dataset RAF-DB (Real-world Affective Faces Database), que contiene más de 30,000 imágenes faciales etiquetadas con 7 categorías de emociones. La arquitectura utiliza una red convolucional (CNN) optimizada para la detección en tiempo real.

## Funcionamiento

1. **Detección facial**: Utilizando el algoritmo Haar Cascade de OpenCV
2. **Preprocesamiento**: Normalización y redimensionamiento de la imagen facial
3. **Predicción**: Aplicación del modelo de IA para determinar la emoción
4. **Estabilización**: Promedio de varias predicciones para mayor precisión
5. **Recomendaciones**: Generación de sugerencias basadas en la emoción detectada

