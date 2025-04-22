# ui_manager.py - Gestión de la interfaz de usuario para la detección de emociones

import cv2
import numpy as np
import time

class UIManager:
    """Clase que gestiona la interfaz de usuario del detector de emociones"""
    
    def __init__(self, detector):
        self.detector = detector
        
        # Colores para cada emoción
        self.emotion_colors = {
            'Sorprendido': (255, 255, 0),   # Amarillo
            'Temeroso': (255, 0, 255),      # Magenta
            'Disgustado': (0, 0, 255),      # Rojo
            'Feliz': (0, 255, 0),           # Verde
            'Triste': (255, 0, 0),          # Azul
            'Enojado': (0, 0, 128),         # Rojo oscuro
            'Neutral': (255, 255, 255)      # Blanco
        }
        
        # Variables para recomendaciones
        self.current_recommendation = None
        self.recommendation_color = (255, 255, 255)
        self.show_music_option = False
        
    def get_emotion_color(self, emotion):
        """Devuelve el color asignado a una emoción"""
        return self.emotion_colors.get(emotion, (0, 255, 0))
        
    def set_recommendation(self, text, color=(255, 255, 255), show_music_option=False):
        """Establece la recomendación actual para mostrar en la interfaz"""
        self.current_recommendation = text
        self.recommendation_color = color
        self.show_music_option = show_music_option
        
    def create_info_panel(self):
        """Crea un panel lateral para mostrar información"""
        panel = np.zeros((self.detector.window_height, self.detector.panel_width, 3), dtype=np.uint8)
        
        # Fondo del panel
        panel[:] = (50, 50, 50)  # Gris oscuro
        
        # Separador
        cv2.line(panel, (0, 0), (0, self.detector.window_height), (200, 200, 200), 1)
        
        # Título
        cv2.putText(panel, "Detector de Emociones", (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Información del modelo
        cv2.putText(panel, "Modelo: RAF-DB", (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Estado actual
        cv2.putText(panel, "Estado:", (20, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(panel, self.detector.instruction, (20, 115), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        # FPS
        cv2.putText(panel, f"FPS: {self.detector.fps:.1f}", (panel.shape[1] - 100, panel.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Si estamos detectando, mostrar tiempo
        if self.detector.detecting:
            elapsed = time.time() - self.detector.start_time
            remaining = max(0, 4 - elapsed)
            
            # Barra de progreso en el panel
            progress = min(elapsed / 4, 1.0) 
            bar_width = self.detector.panel_width - 40
            bar_height = 20
            
            # Texto de tiempo
            cv2.putText(panel, f"Analizando: {remaining:.1f}s", (20, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
            
            # Fondo de la barra
            cv2.rectangle(panel, (20, 160), (20 + bar_width, 160 + bar_height), (100, 100, 100), -1)
            
            # Progreso
            progress_width = int(bar_width * progress)
            if progress < 0.5:
                color = (0, 255, 255)  # Amarillo
            elif progress < 0.75:
                color = (0, 165, 255)  # Naranja
            else:
                color = (0, 255, 0)    # Verde
                
            cv2.rectangle(panel, (20, 160), (20 + progress_width, 160 + bar_height), color, -1)
            
            # Porcentaje
            percentage = int(progress * 100)
            cv2.putText(panel, f"{percentage}%", (20 + bar_width//2 - 15, 160 + bar_height//2 + 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Dibujar resultados de emociones detectadas
        if self.detector.emotion_counter:
            # Título de la sección
            cv2.putText(panel, "Emociones detectadas:", (20, 210), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Calcular totales para porcentajes
            total_detections = sum(self.detector.emotion_counter.values())
            
            # Mostrar cada emoción detectada
            y_pos = 240
            for emotion, count in sorted(self.detector.emotion_counter.items(), key=lambda x: x[1], reverse=True):
                if count == 0:
                    continue
                    
                percentage = int((count / total_detections) * 100) if total_detections > 0 else 0
                color = self.get_emotion_color(emotion)
                
                # Mini barra de progreso para cada emoción
                bar_width = 100
                emotion_width = int((count / max(self.detector.emotion_counter.values())) * bar_width)
                
                # Dibujar nombre y porcentaje
                cv2.putText(panel, f"{emotion}:", (20, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                           
                # Dibujar barra
                cv2.rectangle(panel, (130, y_pos-10), (130+bar_width, y_pos-2), (100, 100, 100), -1)
                cv2.rectangle(panel, (130, y_pos-10), (130+emotion_width, y_pos-2), color, -1)
                
                # Dibujar porcentaje
                cv2.putText(panel, f"{percentage}%", (240, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                y_pos += 25
                
        # Si terminamos la detección, mostrar resultado final
        if self.detector.waiting_for_restart and self.detector.emotion_detected:
            # Fondo para el resultado
            cv2.rectangle(panel, (10, panel.shape[0]-200), (panel.shape[1]-10, panel.shape[0]-50), (0, 0, 0), -1)
            
            # Texto de resultado
            cv2.putText(panel, "Resultado final:", (20, panel.shape[0]-180), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            color = self.get_emotion_color(self.detector.emotion_detected)
            cv2.putText(panel, self.detector.emotion_detected, (20, panel.shape[0]-150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
            
            # Mostrar recomendación actual si hay alguna
            if self.current_recommendation:
                # Dividir la recomendación en múltiples líneas si es necesario
                recommendation_text = self.current_recommendation
                y_pos = panel.shape[0] - 120
                
                # Verificar si el texto es demasiado largo
                if len(recommendation_text) > 35:
                    words = recommendation_text.split()
                    lines = []
                    current_line = ""
                    
                    for word in words:
                        if len(current_line + " " + word) <= 35:
                            current_line += " " + word if current_line else word
                        else:
                            lines.append(current_line)
                            current_line = word
                    
                    if current_line:
                        lines.append(current_line)
                    
                    for line in lines:
                        cv2.putText(panel, line, (20, y_pos), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.recommendation_color, 1)
                        y_pos += 20
                else:
                    cv2.putText(panel, recommendation_text, (20, y_pos), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.recommendation_color, 1)
                    y_pos += 20
                
                # Mostrar opción de música si está activada
                if self.show_music_option:
                    cv2.putText(panel, "Presiona 'M' para escuchar música", (20, y_pos), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            
            # Instrucciones
            cv2.putText(panel, 'R - Reiniciar', (20, panel.shape[0]-70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            cv2.putText(panel, 'Q - Salir', (150, panel.shape[0]-70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                
        return panel
    
    def draw_progress_bar(self, frame, elapsed, total=4):
        """Dibuja una barra de progreso para el tiempo de espera"""
        width = 300
        height = 30
        x = (frame.shape[1] - width) // 2
        y = frame.shape[0] - 80
        
        # Calcular progreso
        progress = min(elapsed / total, 1.0)
        progress_width = int(width * progress)
        
        # Dibujar fondo
        cv2.rectangle(frame, (x, y), (x + width, y + height), (100, 100, 100), -1)
        
        # Dibujar progreso
        if progress < 0.5:
            color = (0, 255, 255)  # Amarillo
        elif progress < 0.75:
            color = (0, 165, 255)  # Naranja
        else:
            color = (0, 255, 0)    # Verde
            
        cv2.rectangle(frame, (x, y), (x + progress_width, y + height), color, -1)
        
        # Dibujar texto
        percentage = int(progress * 100)
        cv2.putText(frame, f"{percentage}%", (x + width//2 - 20, y + height//2 + 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Dibujar borde
        cv2.rectangle(frame, (x, y), (x + width, y + height), (200, 200, 200), 1)