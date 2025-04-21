#!/usr/bin/env python3
# app.py - Archivo principal del detector de emociones

import cv2
from detector import EmotionDetector

def main():
    """Función principal que ejecuta la aplicación de detección de emociones"""
    print("Iniciando Detector de Emociones...")
    
    # Crear instancia del detector
    detector = EmotionDetector()
    
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