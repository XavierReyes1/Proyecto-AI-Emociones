# model_manager.py - Gestión del modelo de IA para la detección de emociones

import os
import cv2
import numpy as np
import threading
import tensorflow as tf

class ModelManager:
    """Clase que gestiona el modelo de reconocimiento de emociones"""
    
    # Etiquetas de emociones según el orden original de RAF-DB
    EMOTION_LABELS = [
        'Sorprendido',  # 0 - Surprise
        'Temeroso',     # 1 - Fear
        'Disgustado',   # 2 - Disgust
        'Feliz',        # 3 - Happy
        'Triste',       # 4 - Sad
        'Enojado',      # 5 - Anger
        'Neutral'       # 6 - Neutral
    ]
    
    def __init__(self, detector):
        self.detector = detector
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), 'modelo_final.keras')
        
    def load_model_async(self):
        """Carga el modelo en un hilo separado"""
        thread = threading.Thread(target=self._load_model)
        thread.daemon = True
        thread.start()
        return thread
        
    def _load_model(self):
        """Implementación de la carga del modelo"""
        try:
            # Configurar TensorFlow para usar menos memoria
            gpus = tf.config.experimental.list_physical_devices('GPU')
            if gpus:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            
            self.detector.instruction = "Cargando modelo de reconocimiento..."
            self.model = tf.keras.models.load_model(self.model_path)
            self.detector.instruction = "Coloca tu rostro frente a la cámara"
        except Exception as e:
            self.detector.instruction = f"Error al cargar el modelo: {e}"
            print(f"Error al cargar modelo: {e}")
    
    def model_ready(self):
        """Verifica si el modelo está listo para ser usado"""
        return self.model is not None
        
    def preprocess_face(self, gray_frame, x, y, w, h):
        """Preprocesa el rostro para la predicción"""
        face = gray_frame[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))
        face = face.astype('float32') / 255.0
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, axis=-1)
        return face
        
    def predict_emotion(self, face_input):
        """Predice la emoción del rostro"""
        if not self.model_ready():
            return None, 0
        
        try:
            prediction = self.model.predict(face_input, verbose=0)
            emotion_idx = np.argmax(prediction)
            return self.EMOTION_LABELS[emotion_idx], prediction[0][emotion_idx]
        except Exception as e:
            print(f"Error al predecir emoción: {e}")
            return None, 0