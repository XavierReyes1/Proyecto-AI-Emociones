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
        
        # Nueva variable para la recomendacion seleccionada
        self.selected_recommendation = {
            'tipo': None,
            'contenido': None,
            'color': None
        }
        
        # Diccionario de recomendaciones por emocion
        self.recommendations = {
            'Feliz': {
                'mensajes': [
                    "Tu felicidad es contagiosa! Sigue asi.",
                    "Aprovecha esta energia positiva para hacer algo que disfrutes.",
                    "Comparte tu alegria con alguien cercano.",
                    "La felicidad te sienta bien. Disfrutala!",
                    "Que bueno verte feliz! Aprovecha el momento."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
                    "https://www.youtube.com/watch?v=ru0K8uYEZWw",
                    "https://www.youtube.com/watch?v=y6Sxv-sUYtM",
                    "https://www.youtube.com/watch?v=09R8_2nJtjg"
                ],
                'acciones': [
                    "Escribe tres cosas por las que estas agradecido hoy",
                    "Llama a un amigo y comparte tu buen humor",
                    "Celebra tu momento feliz con una pequena recompensa",
                    "Toma una foto para recordar este momento feliz"
                ],
                'color': (0, 255, 0)
            },
            'Triste': {
                'mensajes': [
                    "Esta bien sentirse triste a veces. Permite sentir tus emociones.",
                    "Recuerda que todos los sentimientos son temporales.",
                    "Respira profundo. Inhala calma, exhala tension.",
                    "Se amable contigo mismo en los momentos dificiles.",
                    "A veces necesitamos dias nublados para apreciar el sol."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=qeMFqkcPYcg",
                    "https://www.youtube.com/watch?v=5anLPw0Efmo",
                    "https://www.youtube.com/watch?v=WA4iX5D9Z64",
                    "https://www.youtube.com/watch?v=bIB8EWqCPrQ"
                ],
                'acciones': [
                    "Escribe en un diario sobre lo que sientes",
                    "Sal a caminar por 10 minutos al aire libre",
                    "Preparate una taza de te caliente",
                    "Contacta a un ser querido que te haga sentir mejor"
                ],
                'color': (255, 0, 0)
            },
            'Enojado': {
                'mensajes': [
                    "Respira profundamente, inhala por la nariz y exhala por la boca.",
                    "Puedes identificar que desencadeno este sentimiento?",
                    "El enojo a veces nos senala limites que debemos establecer.",
                    "Toma distancia de la situacion si es posible.",
                    "Siente la emocion, pero no permitas que te controle."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=hTWKbfoikeg",
                    "https://www.youtube.com/watch?v=5abamRO41fE",
                    "https://www.youtube.com/watch?v=e-QFj59PON4",
                    "https://www.youtube.com/watch?v=UDVtMYqUAyw"
                ],
                'acciones': [
                    "Haz 10 respiraciones profundas contando hasta 5 en cada inhalacion",
                    "Escribe lo que te molesta en un papel y luego destruyelo",
                    "Realiza ejercicio fisico para liberar tension",
                    "Alejate de la situacion por un momento para calmarte"
                ],
                'color': (0, 0, 128)
            },
            'Temeroso': {
                'mensajes': [
                    "El miedo es una respuesta natural. Reconocelo sin juzgarte.",
                    "Recuerda: has superado situaciones dificiles antes.",
                    "Enfocate en lo que puedes controlar ahora mismo.",
                    "Estas a salvo en este momento. Respira.",
                    "Pequenos pasos te llevan lejos. Cual seria el primero?"
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=lp-EO5I60KA",
                    "https://www.youtube.com/watch?v=UfcAVejslrU",
                    "https://www.youtube.com/watch?v=bJJkEgJU3uE",
                    "https://www.youtube.com/watch?v=9Q634rbsypE"
                ],
                'acciones': [
                    "Practica la tecnica 5-4-3-2-1: nombra 5 cosas que ves, 4 que puedes tocar, 3 que oyes, 2 que hueles y 1 que saboreas",
                    "Visualiza un lugar donde te sientas seguro y tranquilo",
                    "Escribe tus miedos y como podrias afrontarlos",
                    "Realiza un ejercicio de respiracion: inhala 4 segundos, manten 7, exhala 8"
                ],
                'color': (255, 0, 255)
            },
            'Disgustado': {
                'mensajes': [
                    "El disgusto nos ayuda a establecer limites personales.",
                    "Identifica que genera esta emocion y evalua si puedes modificarlo.",
                    "A veces el disgusto senala valores importantes para ti.",
                    "Puedes cambiar la situacion o tu perspectiva sobre ella?",
                    "Toma un momento para reflexionar sobre tus reacciones."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=ZXhuso4OTG4",
                    "https://www.youtube.com/watch?v=jWFWazj7Ud8",
                    "https://www.youtube.com/watch?v=cZnBNuqqz5g",
                    "https://www.youtube.com/watch?v=QxHkLdQy5f0"
                ],
                'acciones': [
                    "Cambia tu entorno: abre una ventana o ve a otro espacio",
                    "Prueba un ejercicio de atencion plena enfocandote en sensaciones agradables",
                    "Toma un pequeno descanso y haz algo que te guste",
                    "Practica la aceptacion de emociones incomodas"
                ],
                'color': (0, 0, 255)
            },
            'Sorprendido': {
                'mensajes': [
                    "La sorpresa nos ayuda a adaptarnos a lo inesperado.",
                    "Aprovecha este estado de alerta para ver las cosas desde una nueva perspectiva.",
                    "Que puedes aprender de esta situacion sorpresiva?",
                    "Lo inesperado a veces trae las mejores oportunidades.",
                    "Respira y date tiempo para procesar lo que ocurre."
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=6JCLY0Rlx6Q",
                    "https://www.youtube.com/watch?v=8UVNT4wvIGY",
                    "https://www.youtube.com/watch?v=1k8craCGpgs",
                    "https://www.youtube.com/watch?v=btPJPFnesV4"
                ],
                'acciones': [
                    "Escribe sobre la situacion que te sorprendio y como te hizo sentir",
                    "Haz una pequena pausa para integrar lo sucedido",
                    "Evalua si necesitas mas informacion para entender mejor la situacion",
                    "Comparte tu experiencia con alguien de confianza"
                ],
                'color': (255, 255, 0)
            },
            'Neutral': {
                'mensajes': [
                    "El estado neutral es perfecto para la introspeccion y planificacion.",
                    "Que actividad te gustaria realizar ahora mismo?",
                    "Un buen momento para establecer metas del dia.",
                    "La calma es un excelente estado para tomar decisiones.",
                    "Como te gustaria sentirte en las proximas horas?"
                ],
                'musica': [
                    "https://www.youtube.com/watch?v=9Aebi-qwl4Q",
                    "https://www.youtube.com/watch?v=5qap5aO4i9A",
                    "https://www.youtube.com/watch?v=jfKfPfyJRdk",
                    "https://www.youtube.com/watch?v=DWcJFNfaw9c"
                ],
                'acciones': [
                    "Establece una pequena meta para hoy",
                    "Realiza una actividad que te brinde satisfaccion",
                    "Toma 5 minutos para meditar o practicar mindfulness",
                    "Reflexiona sobre que actividades te generan mas emociones positivas"
                ],
                'color': (255, 255, 255)
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
    
    def select_recommendation_type(self, emotion):
        """Selecciona un tipo de recomendación basado en las preferencias"""
        # Lista de tipos de recomendación disponibles según preferencias
        available_types = []
        
        if self.detector.preferences.get('show_messages', True):
            available_types.append('mensajes')
        if self.detector.preferences.get('show_actions', True):
            available_types.append('acciones')
        
        # Si hay tipos disponibles, seleccionar uno al azar
        if available_types:
            selected_type = random.choice(available_types)
            return selected_type
        return None

    def select_single_recommendation(self, emotion):
        """Selecciona una sola recomendación entre todos los tipos disponibles"""
        rec_type = self.select_recommendation_type(emotion)
        if not rec_type:
            return False
        
        content = self.get_random_recommendation(emotion, rec_type)
        if not content:
            return False
        
        # Formatear el contenido según el tipo
        formatted_content = content
        if rec_type == 'acciones':
            formatted_content = f"Sugerencia: {content}"
        
        # Guardar la recomendación seleccionada
        self.selected_recommendation = {
            'tipo': rec_type,
            'contenido': formatted_content,
            'color': self.recommendations[emotion]['color']
        }
        
        # Actualizar la UI
        self.detector.ui_manager.set_recommendation(
            formatted_content,
            self.recommendations[emotion]['color'],
            rec_type == 'musica'
        )
        
        return True
    
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
        self.selected_recommendation = {'tipo': None, 'contenido': None, 'color': None}
    
    def _recommendation_loop(self, emotion):
        """Hilo que muestra una sola recomendación"""
        # Seleccionar una recomendación al azar
        self.select_single_recommendation(emotion)
        
        # Si está habilitada la opción de música, mostrarla después de un tiempo
        if self.detector.preferences.get('show_music', True):
            time.sleep(8)  # Mostrar la primera recomendación por 8 segundos
            
            if self.stop_recommendation.is_set():
                return
                
            # Mostrar opción de música
            self.detector.ui_manager.set_recommendation(
                "Presiona 'M' para escuchar música recomendada para este estado emocional", 
                self.recommendations[emotion]['color'],
                True  # Mostrar opción de música
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