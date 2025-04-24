#!/usr/bin/env python3
# app.py - Archivo principal del detector de emociones
import cv2
import tkinter as tk
from tkinter import messagebox, ttk
from detector import EmotionDetector

def show_setup_dialog():
    """Muestra un diálogo para configurar las preferencias de recomendaciones"""
    root = tk.Tk()
    root.title("Configuración del Detector de Emociones")
    root.geometry("400x400")
    root.resizable(False, False)
    
    root.eval('tk::PlaceWindow . center')
    
    # Estilos
    style = ttk.Style()
    style.configure("TRadiobutton", font=("Arial", 12))
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))
    
    # Título
    tk.Label(root, text="Detector de Emociones", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Label(root, text="Selecciona una opción de recomendación:", font=("Arial", 12)).pack(pady=10)
    
    # Variable para opción única
    recommendation_option = tk.StringVar(value="mensajes")  # valor por defecto
    
    options = [
        ("Mostrar mensajes motivacionales", "mensajes"),
        ("Recomendar música según emoción", "musica"),
        ("Sugerir acciones según emoción", "acciones"),
        ("Usar colores según emoción", "colores"),
        ("Recomendaciones aleatorias", "aleatorias")
    ]
    
    for text, value in options:
        ttk.Radiobutton(root, text=text, variable=recommendation_option, value=value).pack(anchor=tk.W, padx=30, pady=5)

    # Variable para controlar si el usuario pulsó iniciar
    user_started = tk.BooleanVar(value=False)

    def on_start():
        user_started.set(True)
        root.destroy()

    def on_cancel():
        root.destroy()

    # Botones
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    ttk.Button(button_frame, text="Iniciar", command=on_start).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Cancelar", command=on_cancel).pack(side=tk.LEFT, padx=10)

    # Nota informativa
    tk.Label(root, text="Nota: Presiona 'Q' para salir de la aplicación\ny 'R' para reiniciar la detección", 
             font=("Arial", 10), fg="gray").pack(pady=20)

    root.mainloop()
    
    if user_started.get():
        # Se devuelve un diccionario para mantener compatibilidad con el detector
        return {
            'show_messages': recommendation_option.get() == "mensajes",
            'show_music': recommendation_option.get() == "musica",
            'show_actions': recommendation_option.get() == "acciones",
            'use_colors': recommendation_option.get() == "colores",
            'random_recommendations': recommendation_option.get() == "aleatorias"
        }
    return None

def main():
    """Función principal que ejecuta la aplicación de detección de emociones"""
    print("Iniciando configuración del Detector de Emociones...")
    
    # Mostrar diálogo de configuración
    preferences = show_setup_dialog()
    
    # Si el usuario canceló, salir
    if preferences is None:
        print("Configuración cancelada por el usuario")
        return
    
    print("Iniciando detector con las siguientes preferencias:")
    for key, value in preferences.items():
        print(f"- {key}: {value}")
    
    # Crear instancia del detector con las preferencias
    detector = EmotionDetector(preferences)
    
    # Ejecutar el detector
    detector.run()
    
    print("Aplicación finalizada")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario")
    except Exception as e:
        print(f"Error inesperado: {e}")