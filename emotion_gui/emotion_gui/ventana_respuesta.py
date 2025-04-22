import random
from tkinter import Tk, Label, Button
import webbrowser

# Recomendaciones por emoción con 5 opciones aleatorias por emoción
recomendaciones = {
    'Angry': [
        ("Respira profundo, escucha algo relajante 😌", "Weightless - Marconi Union"),
        ("Tómate un respiro, escucha algo tranquilo 🌿", "Weightless - Marconi Union"),
        ("Calma tu mente con sonidos suaves 🌊", "Meditation - Moby"),
        ("Respira y relájate con estas melodías 💆‍♂️", "Spiegel Im Spiegel - Arvo Pärt"),
        ("Tranquilo, respira profundamente 🌸", "Calm Your Mind - Relaxation Music"),
    ],
    'Disgust': [
        ("Tal vez una canción suave ayude a despejarte 🎧", "Lo-Fi Chill"),
        ("Relájate con algo suave y tranquilo 🍃", "Lo-Fi Beats"),
        ("Música suave para despejar la mente 🎶", "Calm - Chillhop Music"),
        ("Respira y relájate con melodías suaves 🧘‍♂️", "Peaceful Piano - Relaxing Music"),
        ("Déjate llevar por estas notas relajantes 🌼", "Chill Vibes - LoFi Music"),
    ],
    'Fear': [
        ("Todo estará bien. Escucha algo valiente 🦸", "Titanium - David Guetta ft. Sia"),
        ("Con valentía, enfrenta lo que viene 💪", "Stronger - Kanye West"),
        ("Ponte en marcha con algo inspirador ⚡", "Eye of the Tiger - Survivor"),
        ("Todo lo que necesitas es valor. Escucha esto 🚀", "Warriors - Imagine Dragons"),
        ("Confía, todo va a salir bien. Escucha esto 💫", "Don't Stop Believin' - Journey"),
    ],
    'Happy': [
        ("¡Sigue sonriendo! Aquí va más energía 😄", "Happy - Pharrell Williams"),
        ("Que la felicidad se contagie con esta canción 🎉", "Uptown Funk - Mark Ronson ft. Bruno Mars"),
        ("No pares de bailar con esta música 💃", "Can't Stop the Feeling - Justin Timberlake"),
        ("Disfruta la vida con este ritmo 🎶", "Walking on Sunshine - Katrina and the Waves"),
        ("Sonríe y baila al ritmo de esta canción 🎵", "Shake It Off - Taylor Swift"),
    ],
    'Sad': [
        ("Ánimo, esto puede ayudarte 💪", "Here Comes the Sun - The Beatles"),
        ("Deja que la música te consuele 🌞", "Someone Like You - Adele"),
        ("Recuerda que todo pasará 🌈", "The Scientist - Coldplay"),
        ("Cuando las cosas se pongan difíciles, escucha esto 🧘‍♀️", "Fix You - Coldplay"),
        ("No te rindas, escucha esto para calmarte 🕊", "Let It Be - The Beatles"),
    ],
    'Surprise': [
        ("¡Sorpresas buenas merecen buena música! 🎉", "Can't Stop the Feeling - Justin Timberlake"),
        ("¡Qué sorpresa tan genial! Vamos a celebrarlo 🎉", "Happy - Pharrell Williams"),
        ("Algo inesperado merece una buena canción 🎶", "Viva La Vida - Coldplay"),
        ("Deja que la sorpresa te llene de energía 🎧", "Firework - Katy Perry"),
        ("Lo inesperado trae alegría, escucha esto 🔥", "Roar - Katy Perry"),
    ],
    'Neutral': [
        ("¿Qué tal algo para animar el día? 😊", "Best Day of My Life - American Authors"),
        ("Nada como una canción tranquila para seguir el día 🎶", "Here Comes the Sun - The Beatles"),
        ("Haz que tu día sea mejor con esta melodía 🎧", "Good Life - OneRepublic"),
        ("Para una tarde tranquila, escucha esto 🎶", "Island In The Sun - Weezer"),
        ("Relájate con este tema que te hará sonreír 😄", "Count on Me - Bruno Mars"),
    ]
}

# Emocion detectada (puedes cambiarlo a cualquier emoción que quieras probar)
emocion_detectada = "Happy"  # Cambia esta línea para probar diferentes emociones

# Si la emoción no está en la lista
if emocion_detectada not in recomendaciones:
    print(f"Emoción no reconocida: {emocion_detectada}")
    exit()

# Seleccionamos una recomendación aleatoria
mensaje, cancion = random.choice(recomendaciones[emocion_detectada])

# Interfaz con Tkinter
def mostrar_ventana(emocion, mensaje, cancion):
    root = Tk()
    root.title("Recomendación musical 🎵")
    root.geometry("400x250")
    root.resizable(False, False)

    # Colores personalizados
    root.configure(bg="#e3f2fd")  # Fondo en color azul suave

    # Frame con color de fondo diferente
    frame = Label(root, bg="#2196f3", width=50, height=15)  # Fondo azul fuerte
    frame.pack_propagate(False)  # No permitir que el frame cambie de tamaño
    frame.pack()

    # Etiqueta para mostrar la emoción (color de texto diferente)
    Label(frame, text=f"Emoción: {emocion}", font=("Arial", 16, "bold"), fg="#ffffff", bg="#2196f3").pack(pady=10)

    # Etiqueta para el mensaje de recomendación (color de texto diferente)
    Label(frame, text=mensaje, font=("Arial", 12), wraplength=350, fg="#ffffff", bg="#2196f3").pack(pady=5)

    # Etiqueta para la canción recomendada (color de texto diferente)
    Label(frame, text=f"🎵 {cancion}", font=("Arial", 12, "italic"), fg="#ffffff", bg="#2196f3").pack(pady=5)

    # Función para abrir YouTube
    def abrir_youtube():
        query = cancion.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        root.destroy()  # Cierra la ventana después de abrir YouTube

    # Botón con los colores de YouTube (rojo y blanco) y texto en negrita
    Button(frame, text="Abrir en YouTube", command=abrir_youtube, font=("Arial", 12, "bold"), 
           fg="white", bg="#FF0000", relief="flat", padx=20, pady=10).pack(pady=10)

    root.mainloop()

# Llamar a la función para mostrar la ventana
mostrar_ventana(emocion_detectada, mensaje, cancion)
