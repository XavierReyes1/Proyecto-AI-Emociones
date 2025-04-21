# Proyecto-AI-Emociones


Este proyecto implementa un detector de emociones faciales en tiempo real utilizando un modelo entrenado con el dataset RAF-DB.

## Características

- Detección facial en tiempo real
- Reconocimiento de 7 emociones: Sorprendido, Temeroso, Disgustado, Feliz, Triste, Enojado y Neutral
- Interfaz gráfica con panel informativo separado
- Procesamiento multihilo para mejor rendimiento
- Visualización de estadísticas de detección

## Requisitos

- Python 3.7 o superior
- OpenCV
- TensorFlow 2.x
- NumPy

## Instalación

1. Clonar el repositorio
2. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Descargar o entrenar el modelo y guardarlo como `modelo_final.keras` en el directorio del proyecto

## Uso

Ejecutar el script principal:

```
python app.py
```

### Controles
- `Q`: Salir de la aplicación
- `R`: Reiniciar la detección cuando se muestra un resultado

## Estructura del proyecto

- `app.py`: Punto de entrada de la aplicación
- `detector.py`: Implementación principal del detector de emociones
- `model_manager.py`: Gestión del modelo de IA
- `ui_manager.py`: Gestión de la interfaz de usuario

## Funcionamiento

1. La aplicación carga el modelo de reconocimiento de emociones
2. Captura video desde la cámara web
3. Detecta la posición del rostro
4. Analiza las emociones durante 4 segundos
5. Muestra la emoción más frecuente detectada
