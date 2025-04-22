# detector.py - Clase principal del detector de emociones

import cv2
import numpy as np
import time
import threading
from collections import defaultdict
import os

from model_manager import ModelManager
from ui_manager import UIManager

class EmotionDetector:
    """Clase principal que maneja el detector de emociones faciales"""
    
    def __init__(self):
        # Dimensiones de la interfaz
        self.camera_width = 640
        self.camera_height = 480
        self.panel_width = 320
        self.window_width = self.camera_width + self.panel_width
        self.window_height = self.camera_height
        
        # Estado de la aplicación
        self.detecting = False
        self.start_time = 0
        self.emotion_detected = None
        self.waiting_for_restart = False
        self.instruction = "Iniciando camara y cargando modelo..."
        self.emotion_counter = defaultdict(int)
        self.last_detection_time = 0
        self.detection_interval = 0.5  # Intervalo entre detecciones (segundos)
        
        # Variables para rendimiento
        self.skip_frames = 2
        self.frame_count = 0
        self.running = True
        
        # Variables para multi-threading
        self.frame = None
        self.processed_frame = None
        self.frame_ready = threading.Event()
        self.process_done = threading.Event()
        
        # Métricas
        self.fps = 0
        self.last_fps_update = time.time()
        self.frames_processed = 0
        
        # Inicializar managers
        self.model_manager = ModelManager(self)
        self.ui_manager = UIManager(self)
        
        # Variables de captura
        self.cap = None
        self.face_cascade = None
        
    def initialize(self):
        """Inicializa los recursos necesarios"""
        try:
            # Inicializar detector de rostros
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if self.face_cascade.empty():
                raise Exception("No se pudo cargar el detector de rostros")
            
            # Inicializar cámara
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("No se pudo abrir la cámara")
            
            # Configurar resolución de la cámara
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
            
            # Iniciar carga del modelo en un hilo separado
            self.model_manager.load_model_async()
                
            return True
        except Exception as e:
            print(f"Error al inicializar: {e}")
            return False
    
    def preprocess_face(self, gray_frame, x, y, w, h):
        """Preprocesa el rostro para la prediccion"""
        return self.model_manager.preprocess_face(gray_frame, x, y, w, h)

    def get_most_frequent_emotion(self):
        """Obtiene la emocion mas frecuente detectada durante el periodo"""
        if not self.emotion_counter:
            return None
        return max(self.emotion_counter.items(), key=lambda x: x[1])[0]
    
    def process_frame(self, frame):
        """Procesa un frame de la camara"""
        # Crear un lienzo para la interfaz completa
        display = np.zeros((self.window_height, self.window_width, 3), dtype=np.uint8)
        
        # Colocar el frame de la cámara en el lado izquierdo
        display[:, :self.camera_width] = frame
        
        # No procesar completamente si no hay modelo
        if not self.model_manager.model_ready():
            # Crear panel de información
            info_panel = self.ui_manager.create_info_panel()
            display[:, self.camera_width:] = info_panel
            return display
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Solo procesamos cada N frames para mejor rendimiento
        if self.frame_count % self.skip_frames != 0 and not self.waiting_for_restart:
            self.frame_count += 1
            
            # Crear panel de información
            info_panel = self.ui_manager.create_info_panel()
            display[:, self.camera_width:] = info_panel
            
            return display
            
        self.frame_count += 1
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if not self.waiting_for_restart:
            if len(faces) == 0:
                self.instruction = "Coloca tu rostro frente a la camara"
                self.detecting = False
                self.emotion_counter.clear()
            else:
                # Encontrar el rostro más grande (asumiendo que es el principal)
                if len(faces) > 1:
                    faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
                
                for (x, y, w, h) in faces[:1]:  # Procesar solo el rostro más grande
                    frame_height, frame_width = frame.shape[:2]
                    
                    # Dibujar rectángulo alrededor del rostro
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                    # Verificar posición del rostro
                    if w < frame_width * 0.2:
                        self.instruction = "Acercate un poco mas"
                        self.detecting = False
                        self.emotion_counter.clear()
                    elif x < frame_width * 0.2:
                        self.instruction = "Muevete hacia la derecha"
                        self.detecting = False
                        self.emotion_counter.clear()
                    elif (x + w) > frame_width * 0.8:
                        self.instruction = "Muevete hacia la izquierda"
                        self.detecting = False
                        self.emotion_counter.clear()
                    else:
                        self.instruction = "Perfecto, mantente asi"
                        if not self.detecting:
                            self.start_time = time.time()
                            self.detecting = True
                            self.emotion_counter.clear()

                        # Procesar emociones periódicamente
                        current_time = time.time()
                        if self.detecting and (current_time - self.last_detection_time) >= self.detection_interval:
                            face_input = self.preprocess_face(gray, x, y, w, h)
                            current_emotion, confidence = self.model_manager.predict_emotion(face_input)
                            if current_emotion:
                                self.emotion_counter[current_emotion] += 1
                                self.last_detection_time = current_time

                                # Mostrar etiqueta de emoción actual sobre el rostro
                                emotion_label = f"{current_emotion}"
                                text_size = cv2.getTextSize(emotion_label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
                                cv2.rectangle(frame, (x, y-text_size[1]-5), (x+text_size[0]+10, y), 
                                             self.ui_manager.get_emotion_color(current_emotion), -1)
                                cv2.putText(frame, emotion_label, (x+5, y-5), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

                        # Esperar 4 segundos de estabilidad
                        if self.detecting and (current_time - self.start_time) >= 4:
                            self.emotion_detected = self.get_most_frequent_emotion()
                            self.waiting_for_restart = True
                            self.detecting = False
                    
        # Si terminamos y tenemos resultado
        if self.waiting_for_restart and self.emotion_detected:
            # Mostrar resultado en el frame principal
            color = self.ui_manager.get_emotion_color(self.emotion_detected)
            cv2.putText(frame, self.emotion_detected, (frame.shape[1]//2 - 100, frame.shape[0]//2), 
                       cv2.FONT_HERSHEY_DUPLEX, 1.5, color, 2)

        # Crear panel de información
        info_panel = self.ui_manager.create_info_panel()
        
        # Actualizar FPS
        self.frames_processed += 1
        current_time = time.time()
        if current_time - self.last_fps_update >= 1.0:
            self.fps = self.frames_processed / (current_time - self.last_fps_update)
            self.frames_processed = 0
            self.last_fps_update = current_time
            
        # Combinar frame y panel en la pantalla final
        display[:, self.camera_width:] = info_panel

        return display
        
    def processing_thread(self):
        """Hilo para procesar los frames"""
        while self.running:
            self.frame_ready.wait()
            if not self.running:
                break
                
            if self.frame is not None:
                self.processed_frame = self.process_frame(self.frame.copy())
                
            self.frame_ready.clear()
            self.process_done.set()
    
    def run(self):
        """Ejecuta el detector de emociones"""
        if not self.initialize():
            print("Error al inicializar los recursos")
            return
            
        # Iniciar hilo de procesamiento
        process_thread = threading.Thread(target=self.processing_thread)
        process_thread.start()
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error al leer frame de la camara")
                    break
                    
                # Voltear horizontalmente para efecto espejo
                frame = cv2.flip(frame, 1)
                
                # Pasar frame al hilo de procesamiento
                self.frame = frame
                self.frame_ready.set()
                self.process_done.wait()
                self.process_done.clear()
                
                # Mostrar el frame procesado
                if self.processed_frame is not None:
                    cv2.imshow('Detector de Emociones (RAF-DB)', self.processed_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                if key == ord('r') and self.waiting_for_restart:
                    self.waiting_for_restart = False
                    self.emotion_detected = None
                    self.detecting = False
                    self.instruction = "Coloca tu rostro frente a la camara"
                    self.emotion_counter.clear()
                    
        except KeyboardInterrupt:
            pass
        finally:
            # Liberar recursos
            self.running = False
            self.frame_ready.set()  # Desbloquear el hilo de procesamiento
            process_thread.join()
            
            if self.cap is not None:
                self.cap.release()
            cv2.destroyAllWindows()
            print("Aplicación terminada")