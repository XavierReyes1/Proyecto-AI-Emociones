# recommendation_manager.py - Gestor de recomendaciones basadas en el estado emocional

import random
import webbrowser
import threading
import time
import os
import json
from datetime import datetime

class RecommendationManager:
    """Clase que gestiona recomendaciones personalizadas basadas en el estado emocional"""
    
    def __init__(self, detector):
        self.detector = detector
        self.current_emotion = None
        self.recommendations_active = False
        self.recommendation_thread = None
        self.stop_recommendation = threading.Event()
        
        # Ruta para guardar el historial de emociones
        self.history_file = os.path.join(os.path.dirname(__file__), 'emotion_history.json')
        
        # Diccionario de recomendaciones por emoción
        self.recommendations = {
            'Feliz': {
                'mensajes': [
                    "¡Tu felicidad es contagiosa! Sigue así.",
                    "Aprovecha esta energía positiva para hacer algo que disfrutes.",
                    "Comparte tu alegría con alguien cercano.",
                    "La felicidad te sienta bien. ¡Disfrútala!",
                    "¡Qué bueno verte feliz! Aprovecha el momento."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=ZbZSe6N_BXs",  # Happy - Pharrell Williams
                    "https://www.youtube.com/watch?v=ru0K8uYEZWw",  # Good Feeling - Flo Rida
                    "https://www.youtube.com/watch?v=y6Sxv-sUYtM",  # Happy - Pharrell Williams
                    "https://www.youtube.com/watch?v=09R8_2nJtjg"   # Uptown Funk - Mark Ronson ft. Bruno Mars
                ],
                'acciones': [
                    "Escribe tres cosas por las que estás agradecido hoy",
                    "Llama a un amigo y comparte tu buen humor",
                    "Celebra tu momento feliz con una pequeña recompensa",
                    "Toma una foto para recordar este momento feliz"
                ],
                'color': (0, 255, 0)  # Verde
            },
            'Triste': {
                'mensajes': [
                    "Está bien sentirse triste a veces. Permite sentir tus emociones.",
                    "Recuerda que todos los sentimientos son temporales.",
                    "Respira profundo. Inhala calma, exhala tensión.",
                    "Sé amable contigo mismo en los momentos difíciles.",
                    "A veces necesitamos días nublados para apreciar el sol."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=qeMFqkcPYcg",  # Sweet Dreams - Eurythmics
                    "https://www.youtube.com/watch?v=5anLPw0Efmo",  # Everybody Hurts - R.E.M.
                    "https://www.youtube.com/watch?v=WA4iX5D9Z64",  # Fix You - Coldplay
                    "https://www.youtube.com/watch?v=bIB8EWqCPrQ"   # The Scientist - Coldplay
                ],
                'acciones': [
                    "Escribe en un diario sobre lo que sientes",
                    "Sal a caminar por 10 minutos al aire libre",
                    "Prepárate una taza de té caliente",
                    "Contacta a un ser querido que te haga sentir mejor"
                ],
                'color': (255, 0, 0)  # Azul
            },
            'Enojado': {
                'mensajes': [
                    "Respira profundamente, inhala por la nariz y exhala por la boca.",
                    "¿Puedes identificar qué desencadenó este sentimiento?",
                    "El enojo a veces nos señala límites que debemos establecer.",
                    "Toma distancia de la situación si es posible.",
                    "Siente la emoción, pero no permitas que te controle."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=hTWKbfoikeg",  # Smells Like Teen Spirit - Nirvana
                    "https://www.youtube.com/watch?v=5abamRO41fE",  # Música de relajación
                    "https://www.youtube.com/watch?v=e-QFj59PON4",  # Música para calmar la ira
                    "https://www.youtube.com/watch?v=UDVtMYqUAyw"   # Música de meditación
                ],
                'acciones': [
                    "Haz 10 respiraciones profundas contando hasta 5 en cada inhalación",
                    "Escribe lo que te molesta en un papel y luego destrúyelo",
                    "Realiza ejercicio físico para liberar tensión",
                    "Aléjate de la situación por un momento para calmarte"
                ],
                'color': (0, 0, 128)  # Rojo oscuro
            },
            'Temeroso': {
                'mensajes': [
                    "El miedo es una respuesta natural. Reconócelo sin juzgarte.",
                    "Recuerda: has superado situaciones difíciles antes.",
                    "Enfócate en lo que puedes controlar ahora mismo.",
                    "Estás a salvo en este momento. Respira.",
                    "Pequeños pasos te llevan lejos. ¿Cuál sería el primero?"
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=lp-EO5I60KA",  # Weightless - Marconi Union
                    "https://www.youtube.com/watch?v=UfcAVejslrU",  # Música relajante
                    "https://www.youtube.com/watch?v=bJJkEgJU3uE",  # Música para reducir ansiedad
                    "https://www.youtube.com/watch?v=9Q634rbsypE"   # Música para calmar el miedo
                ],
                'acciones': [
                    "Practica la técnica 5-4-3-2-1: nombra 5 cosas que ves, 4 que puedes tocar, 3 que oyes, 2 que hueles y 1 que saboreas",
                    "Visualiza un lugar donde te sientas seguro y tranquilo",
                    "Escribe tus miedos y cómo podrías afrontarlos",
                    "Realiza un ejercicio de respiración: inhala 4 segundos, mantén 7, exhala 8"
                ],
                'color': (255, 0, 255)  # Magenta
            },
            'Disgustado': {
                'mensajes': [
                    "El disgusto nos ayuda a establecer límites personales.",
                    "Identifica qué genera esta emoción y evalúa si puedes modificarlo.",
                    "A veces el disgusto señala valores importantes para ti.",
                    "¿Puedes cambiar la situación o tu perspectiva sobre ella?",
                    "Toma un momento para reflexionar sobre tus reacciones."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=ZXhuso4OTG4",  # Música para elevar el ánimo
                    "https://www.youtube.com/watch?v=jWFWazj7Ud8",  # Música de relajación
                    "https://www.youtube.com/watch?v=cZnBNuqqz5g",  # Música para cambiar el estado de ánimo
                    "https://www.youtube.com/watch?v=QxHkLdQy5f0"   # Música para bienestar
                ],
                'acciones': [
                    "Cambia tu entorno: abre una ventana o ve a otro espacio",
                    "Prueba un ejercicio de atención plena enfocándote en sensaciones agradables",
                    "Toma un pequeño descanso y haz algo que te guste",
                    "Practica la aceptación de emociones incómodas"
                ],
                'color': (0, 0, 255)  # Rojo
            },
            'Sorprendido': {
                'mensajes': [
                    "La sorpresa nos ayuda a adaptarnos a lo inesperado.",
                    "Aprovecha este estado de alerta para ver las cosas desde una nueva perspectiva.",
                    "¿Qué puedes aprender de esta situación sorpresiva?",
                    "Lo inesperado a veces trae las mejores oportunidades.",
                    "Respira y date tiempo para procesar lo que ocurre."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=6JCLY0Rlx6Q",  # Feel It Still - Portugal. The Man
                    "https://www.youtube.com/watch?v=8UVNT4wvIGY",  # Somebody That I Used To Know - Gotye
                    "https://www.youtube.com/watch?v=1k8craCGpgs",  # Don't Stop Me Now - Queen
                    "https://www.youtube.com/watch?v=btPJPFnesV4"   # Eye of the Tiger - Survivor
                ],
                'acciones': [
                    "Escribe sobre la situación que te sorprendió y cómo te hizo sentir",
                    "Haz una pequeña pausa para integrar lo sucedido",
                    "Evalúa si necesitas más información para entender mejor la situación",
                    "Comparte tu experiencia con alguien de confianza"
                ],
                'color': (255, 255, 0)  # Amarillo
            },
            'Neutral': {
                'mensajes': [
                    "El estado neutral es perfecto para la introspección y planificación.",
                    "¿Qué actividad te gustaría realizar ahora mismo?",
                    "Un buen momento para establecer metas del día.",
                    "La calma es un excelente estado para tomar decisiones.",
                    "¿Cómo te gustaría sentirte en las próximas horas?"
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=9Aebi-qwl4Q",  # Lo-fi beats
                    "https://www.youtube.com/watch?v=5qap5aO4i9A",  # Música para estudiar
                    "https://www.youtube.com/watch?v=jfKfPfyJRdk",  # Música para concentrarse
                    "https://www.youtube.com/watch?v=DWcJFNfaw9c"   # Música ambiental
                ],
                'acciones': [
                    "Establece una pequeña meta para hoy",
                    "Realiza una actividad que te brinde satisfacción",
                    "Toma 5 minutos para meditar o practicar mindfulness",
                    "Reflexiona sobre qué actividades te generan más emociones positivas"
                ],
                'color': (255, 255, 255)  # Blanco
            }
        }
        
        # Cargar historial de emociones si existe
        self.emotion_history = self._load_emotion_history()
    
    def _load_emotion_history(self):
        """Carga el historial de emociones desde un archivo json"""
        if not os.path.exists(self.history_file):
            return {}
        
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar historial de emociones: {e}")
            return {}
    
    def _save_emotion_history(self):
        """Guarda el historial de emociones en un archivo json"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.emotion_history, f, indent=2)
        except Exception as e:
            print(f"Error al guardar historial de emociones: {e}")
    
    def update_emotion_history(self, emotion):
        """Actualiza el historial de emociones"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.emotion_history:
            self.emotion_history[today] = {}
        
        if emotion not in self.emotion_history[today]:
            self.emotion_history[today][emotion] = 0
        
        self.emotion_history[today][emotion] += 1
        self._save_emotion_history()
    
    def get_random_recommendation(self, emotion, rec_type):
        """Obtiene una recomendación aleatoria del tipo y emoción especificados"""
        if emotion in self.recommendations and rec_type in self.recommendations[emotion]:
            recommendations = self.recommendations[emotion][rec_type]
            return random.choice(recommendations)
        return None
    
    def start_recommendations(self, emotion):
        """Inicia el proceso de recomendaciones para una emoción detectada"""
        if emotion != self.current_emotion:
            self.current_emotion = emotion
            self.update_emotion_history(emotion)
            
            # Detener hilo de recomendaciones anterior si existe
            if self.recommendation_thread and self.recommendation_thread.is_alive():
                self.stop_recommendation.set()
                self.recommendation_thread.join(timeout=1)
                self.stop_recommendation.clear()
            
            # Iniciar nuevo hilo de recomendaciones
            self.recommendations_active = True
            self.recommendation_thread = threading.Thread(
                target=self._recommendation_loop, 
                args=(emotion,)
            )
            self.recommendation_thread.daemon = True
            self.recommendation_thread.start()
            
            return True
        return False
    
    def stop_recommendations(self):
        """Detiene el proceso de recomendaciones"""
        self.recommendations_active = False
        if self.recommendation_thread and self.recommendation_thread.is_alive():
            self.stop_recommendation.set()
            self.recommendation_thread.join(timeout=1)
            self.stop_recommendation.clear()
        self.current_emotion = None
    
    def _recommendation_loop(self, emotion):
        """Hilo que muestra recomendaciones periódicamente"""
        # Mostrar mensaje inicial
        mensaje = self.get_random_recommendation(emotion, 'mensajes')
        self.detector.ui_manager.set_recommendation(mensaje, self.recommendations[emotion]['color'])
        
        # Esperar un tiempo antes de mostrar recomendación de acción
        time.sleep(5)
        if self.stop_recommendation.is_set():
            return
            
        # Mostrar recomendación de acción
        accion = self.get_random_recommendation(emotion, 'acciones')
        self.detector.ui_manager.set_recommendation(f"Sugerencia: {accion}", self.recommendations[emotion]['color'])
        
        # Preguntar si quiere música
        time.sleep(5)
        if self.stop_recommendation.is_set():
            return
            
        # Mostrar opción de música
        self.detector.ui_manager.set_recommendation(
            "Presiona 'M' para escuchar música recomendada para este estado emocional", 
            self.recommendations[emotion]['color'],
            show_music_option=True
        )
    
    def play_music_recommendation(self):
        """Reproduce música recomendada para la emoción actual"""
        if not self.current_emotion:
            return
            
        url = self.get_random_recommendation(self.current_emotion, 'musica')
        if url:
            try:
                webbrowser.open(url)
                return True
            except Exception as e:
                print(f"Error al abrir el navegador: {e}")
        return False
    
    def get_emotion_statistics(self):
        """Devuelve estadísticas de emociones para mostrar en la interfaz"""
        stats = {
            'hoy': {},
            'total': {}
        }
        
        # Obtener estadísticas del día de hoy
        today = datetime.now().strftime("%Y-%m-%d")
        if today in self.emotion_history:
            stats['hoy'] = self.emotion_history[today]
        
        # Calcular estadísticas totales
        for day, emotions in self.emotion_history.items():
            for emotion, count in emotions.items():
                if emotion not in stats['total']:
                    stats['total'][emotion] = 0
                stats['total'][emotion] += count
        
        return stats
    
    def get_emotion_report(self):
        """Genera un informe sobre las emociones del usuario"""
        stats = self.get_emotion_statistics()
        report = "Informe de emociones\n"
        report += "-----------------\n\n"
        
        # Emociones de hoy
        report += "Hoy:\n"
        if stats['hoy']:
            total_hoy = sum(stats['hoy'].values())
            for emotion, count in sorted(stats['hoy'].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_hoy) * 100
                report += f"- {emotion}: {count} veces ({percentage:.1f}%)\n"
        else:
            report += "No hay datos para hoy\n"
        
        report += "\nHistorial general:\n"
        if stats['total']:
            total = sum(stats['total'].values())
            for emotion, count in sorted(stats['total'].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total) * 100
                report += f"- {emotion}: {count} veces ({percentage:.1f}%)\n"
        else:
            report += "No hay datos históricos\n"
        
        # Añadir recomendaciones personalizadas basadas en emociones predominantes
        report += "\nRecomendaciones personalizadas:\n"
        if stats['total']:
            # Encontrar la emoción más frecuente
            dominant_emotion = max(stats['total'].items(), key=lambda x: x[1])[0]
            
            if dominant_emotion == 'Feliz':
                report += "- Continúa con actividades que te generan alegría\n"
                report += "- Comparte tu bienestar con otros\n"
                report += "- Establece metas positivas para mantener este estado\n"
            elif dominant_emotion in ['Triste', 'Enojado', 'Temeroso', 'Disgustado']:
                report += "- Considera practicar técnicas de mindfulness o meditación\n"
                report += "- El ejercicio físico puede ayudar a regular tus emociones\n"
                report += "- Busca actividades que te conecten con emociones positivas\n"
            else:
                report += "- Mantén un equilibrio entre actividades y descanso\n"
                report += "- Explora nuevas actividades que te generen interés\n"
                report += "- Establece rutinas que favorezcan tu bienestar emocional\n"
        
        return report
    
    def export_emotion_history(self, filename):
        """Exporta el historial de emociones a un archivo CSV"""
        try:
            with open(filename, 'w') as f:
                f.write("Fecha,Emoción,Frecuencia\n")
                for date, emotions in self.emotion_history.items():
                    for emotion, count in emotions.items():
                        f.write(f"{date},{emotion},{count}\n")
            return True
        except Exception as e:
            print(f"Error al exportar historial: {e}")
            return False