import cv2
import numpy as np
import tensorflow as tf
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import os

# Cargar el modelo entrenado
model = tf.keras.models.load_model(r"C:\\Users\\laine\\OneDrive\\Documentos\\emotion_gui\\emotion_gui\\fer_pro_model_final.keras")
#model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
emotion_labels = ['Enojo', 'Disgusto', 'Miedo', 'Feliz', 'Sorpresa', 'Triste', 'Neutral']


# Variables globales
cap = None
running = False
video_label = None
main_window = None


def preprocess_face(face):
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(face, (48, 48))
    face = face.astype("float32") / 255.0
    face = np.expand_dims(face, axis=0)
    face = np.expand_dims(face, axis=-1)
    return face

def detect_and_predict():
    if running:
        ret, frame = cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') \
                    .detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = frame[y:y+h, x:x+w]
            preprocessed = preprocess_face(roi)
            preds = model.predict(preprocessed)

            print("Predicciones:", preds)
            print("Índice máximo:", np.argmax(preds))
            print("Emoción detectada:", emotion_labels[np.argmax(preds)])

            emotion = emotion_labels[np.argmax(preds)]

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Mostrar imagen en la GUI
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    main_window.after(10, detect_and_predict)

def stop():
    global running
    running = False
    cap.release()
    if main_window:  # Verificar si main_window aún existe
        main_window.destroy()
    ventana_inicio.destroy()




# Ventana Principal
def iniciar_ventana_principal():
    global main_window, video_label, running, cap

    ventana_inicio.destroy()

    # Crear la ventana principal
    main_window = Tk()
    main_window.configure(bg="#1e1e2f")
    main_window.title("Reconocimiento de Emociones")
    main_window.geometry("800x600")

    # Widget para mostrar el video
    video_label = Label(main_window, bg="#1e1e2f")
    video_label.pack()

    # Botón para cerrar la app
    Button(
        main_window, text="Salir", command=stop,
        font=("Arial", 16), bg="#3e8ed0", fg="white",
        activebackground="#2f6ca4", activeforeground="white"
    ).pack(pady=10)

    # Captura de la cámara
    cap = cv2.VideoCapture(0)
    running = True

    # Iniciar la detección
    detect_and_predict()
    main_window.mainloop()




#  -----------GIF---------
def mostrar_splash_con_gif():
    splash = Tk()
    splash.overrideredirect(True)  # Sin bordes ni barra de título
    splash.geometry("600x550+500+100")
    splash.configure(bg="#1e1e2f")

    # Título estilo logo o encabezado
    label_titulo = Label(
        splash,
        text="",
        font=("Arial", 18, "bold"),
        bg="#1e1e2f",
        fg="#f5f5f5",
        pady=10
    )
    label_titulo.pack()

    # Cargar GIF animado
    gif = Image.open(r"C:\\Users\\laine\\OneDrive\\Documentos\\emotion_gui\\emotion_gui\\RGRk.gif")
    frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

    # Etiqueta para el GIF
    label_gif = Label(splash, bg="#1e1e2f")
    label_gif.pack(pady=10)

    # Etiqueta para el texto animado
    label_texto = Label(splash, text="Cargando", font=("Arial", 20), bg="#1e1e2f", fg="#3e8ed0")
    label_texto.pack()

    def animar_gif(index):
        if not splash.winfo_exists():
            return  # Si la ventana splash ya no existe, detener la animación.
        frame = frames[index]
        label_gif.configure(image=frame)
        splash.after(100, animar_gif, (index + 1) % len(frames))

    def animar_texto(puntos=0):
        if not splash.winfo_exists():
            return  # Si la ventana splash ya no existe, detener la animación.
        texto = "Cargando" + ("." * puntos)
        label_texto.configure(text=texto)
        splash.after(500, animar_texto, (puntos + 1) % 4)

    def escribir_texto(titulo, index=0):
        if index <= len(titulo):
            label_titulo.configure(text=titulo[:index])
            splash.after(100, escribir_texto, titulo, index + 1)

    animar_gif(0)
    animar_texto()
    escribir_texto("🎭 Detector de Emociones")

    def cerrar_splash():
        if splash.winfo_exists():  # Solo cerrar si la ventana aún existe
            splash.after(4000, splash.destroy)


    splash.after(4000, cerrar_splash)  # Esta es la forma más limpia
    splash.mainloop()

# Llamar splash antes de la ventana de inicio
mostrar_splash_con_gif()




# -------------------- Pantalla de inicio --------------------
ventana_inicio = Tk()
ventana_inicio.title("Bienvenido")
ventana_inicio.geometry("800x400")
#ventana_inicio.configure(bg="#1e1e2f")  # Fondo oscuro elegante
ventana_inicio.resizable(False, False)

# Cargar fondo si existe
ruta_imagen = r"C:\\Users\\laine\\OneDrive\\Documentos\\emotion_gui\\emotion_gui\\Emo1.jpg"

# Crear Canvas
canvas = Canvas(ventana_inicio, width=800, height=400)
canvas.pack(fill="both", expand=True)

# Cargar fondo si existe
if os.path.exists(ruta_imagen):
    fondo_img = Image.open(ruta_imagen)
    fondo_img = fondo_img.resize((800, 400))
    fondo_tk = ImageTk.PhotoImage(fondo_img)
    canvas.create_image(0, 0, image=fondo_tk, anchor="nw")

# Simular capa translúcida con un rectángulo gris con opacidad simulada
canvas.create_rectangle(0, 0, 800, 400, fill="#1e1e2f", stipple="gray25")

# ----------- Título con sombra -----------

# Sombra (desplazada ligeramente)
canvas.create_text(402, 82, text="🎭 Detector de Emociones en Tiempo Real",
                   fill="black", font=("Arial", 22, "bold"))

# Texto principal
canvas.create_text(400, 80, text="🎭 Detector de Emociones en Tiempo Real",
                   fill="white", font=("Arial", 22, "bold"))

# ----------- Subtítulo con sombra -----------

# Sombra
canvas.create_text(402, 142, text="Analiza emociones a través de tu cámara",
                   fill="black", font=("Arial", 14))

# Texto principal
canvas.create_text(400, 140, text="Analiza emociones a través de tu cámara",
                   fill="white", font=("Arial", 14))


# ---------- Botón con efecto hover ----------
def on_enter(e):
    boton_inicio.config(bg="#d43f3a")  # Rojo fuerte

def on_leave(e):
    boton_inicio.config(bg="#3e8ed0")  # Azul original

def iniciar():
    ventana_inicio.withdraw()
    iniciar_ventana_principal()
    
boton_inicio = Button(ventana_inicio,
                      text="Iniciar",
                      font=("Arial Black", 14, "bold"),
                      bg="#3e8ed0",
                      fg="white",
                      activebackground="#d43f3a",
                      activeforeground="white",
                      width=15,
                      height=2,
                      command=iniciar,
                      relief="flat",
                      cursor="hand2")

# Insertar el botón dentro del canvas
canvas.create_window(400, 220, window=boton_inicio)

# Eventos hover
boton_inicio.bind("<Enter>", on_enter)
boton_inicio.bind("<Leave>", on_leave)

ventana_inicio.mainloop()