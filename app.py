import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model

# Cargar el modelo entrenado
model = load_model('emotion_detection_model.keras')

# Definir etiquetas de emociones
emotion_labels = ['Enojado', 'Disgustado', 'Temeroso', 'Feliz', 'Triste', 'Sorprendido', 'Neutral']

# Cargar el detector de rostros de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Variables para control de tiempo y estado
detecting = False
start_time = 0
emotion_detected = None
waiting_for_restart = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if not waiting_for_restart:
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (48, 48))
            face = face.astype('float32') / 255.0
            face = np.expand_dims(face, axis=0)
            face = np.expand_dims(face, axis=-1)

            if not detecting:
                start_time = time.time()
                detecting = True

            if detecting and (time.time() - start_time) >= 4:
                # Después de 4 segundos, predecir emoción
                prediction = model.predict(face)
                emotion_idx = np.argmax(prediction)
                emotion_detected = emotion_labels[emotion_idx]
                waiting_for_restart = True
                detecting = False

            # Dibujar rectángulo en la cara detectada
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    else:
        # Mostrar emoción detectada
        if emotion_detected:
            cv2.putText(frame, f'Emocion: {emotion_detected}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3, cv2.LINE_AA)
            cv2.putText(frame, 'Presiona "r" para reiniciar', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)

    cv2.imshow('Detector de Emociones', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('r') and waiting_for_restart:
        waiting_for_restart = False
        emotion_detected = None
        detecting = False

# Liberar recursos
cap.release()
cv2.destroyAllWindows()