
# ui_manager.py - Gestión de la interfaz de usuario para la detección de emociones

import cv2
import numpy as np
import time

class UIManager:
    """Clase que gestiona la interfaz de usuario del detector de emociones"""
    
    def __init__(self, detector):
        self.detector = detector
        
        # Colores para cada emoción en formato BGR (Blue, Green, Red)
        self.emotion_colors = {
            'Sorprendido': (0, 255, 255),    # Amarillo
            'Temeroso': (255, 0, 255),       # Magenta
            'Disgustado': (255, 0, 0),       # Azul
            'Feliz': (0, 255, 0),            # Verde
            'Triste': (0, 0, 255),           # Rojo
            'Enojado': (128, 0, 0),          # Azul oscuro
            'Neutral': (255, 255, 255)       # Blanco
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
            # Crear un fondo más grande para la recomendación
            rec_panel_height = 280  # Altura del panel para recomendaciones
            rec_panel_y = panel.shape[0] - rec_panel_height - 30
            cv2.rectangle(panel, (10, rec_panel_y), (panel.shape[1]-10, panel.shape[0]-30), (30, 30, 30), -1)
            cv2.rectangle(panel, (10, rec_panel_y), (panel.shape[1]-10, panel.shape[0]-30), (100, 100, 100), 1)
            
            # Texto de resultado
            cv2.putText(panel, "Resultado final:", (20, rec_panel_y + 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            color = self.get_emotion_color(self.detector.emotion_detected)
            cv2.putText(panel, self.detector.emotion_detected, (20, rec_panel_y + 55), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
            
            # Mostrar solo la recomendación seleccionada
            if self.detector.emotion_detected and hasattr(self.detector, 'recommendation_manager'):
                rec_manager = self.detector.recommendation_manager
                
                if rec_manager.selected_recommendation['contenido']:
                    y_pos = rec_panel_y + 90
                    
                    # Título según el tipo de recomendación
                    if rec_manager.selected_recommendation['tipo'] == 'mensajes':
                        cv2.putText(panel, "Mensaje:", (20, y_pos),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
                    elif rec_manager.selected_recommendation['tipo'] == 'acciones':
                        cv2.putText(panel, "Sugerencia:", (20, y_pos),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
                    
                    y_pos += 25
                    
                    # Mostrar el contenido de la recomendación seleccionada
                    self._draw_wrapped_text(panel, rec_manager.selected_recommendation['contenido'], 
                                        (20, y_pos), (255, 255, 255), 0.55, 
                                        self.detector.panel_width - 40)
            
            # Opción de música
            if hasattr(self.detector, 'recommendation_manager') and self.detector.preferences.get('show_music', True):
                rec_manager = self.detector.recommendation_manager
                emotion = self.detector.emotion_detected
                
                if emotion in rec_manager.recommendations and rec_manager.recommendations[emotion].get('musica', []):
                    # Crear un botón visual para la música
                    music_btn_y = panel.shape[0] - 75
                    music_btn_height = 30
                    cv2.rectangle(panel, (20, music_btn_y), (panel.shape[1] - 20, music_btn_y + music_btn_height), 
                                (0, 128, 255), -1)
                    cv2.putText(panel, "Presiona 'M' para escuchar música recomendada", 
                            (30, music_btn_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Instrucciones en la parte inferior
            cv2.putText(panel, 'R - Reiniciar', (20, panel.shape[0]-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            cv2.putText(panel, 'Q - Salir', (150, panel.shape[0]-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                
        return panel

    def _draw_wrapped_text(self, img, text, pos, color, font_scale, max_width):
        """Dibuja texto con ajuste de línea"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        line_height = int(font_scale * 30)
        x, y = pos
        
        # Dividir el texto en palabras
        words = text.split()
        if not words:
            return y
        
        # Construir líneas que quepan en max_width
        lines = []
        current_line = words[0]
        for word in words[1:]:
            # Estimar el ancho del texto con getTextSize
            test_line = current_line + ' ' + word
            (test_width, _), _ = cv2.getTextSize(test_line, font, font_scale, 1)
            
            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        
        # Dibujar cada línea
        for i, line in enumerate(lines):
            cv2.putText(img, line, (x, y + i * line_height), font, font_scale, color, 1)
        
        return y + len(lines) * line_height
    
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