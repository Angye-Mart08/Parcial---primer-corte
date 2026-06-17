import tkinter as tk
import threading
import time
import random

ventana = tk.Tk()
ventana.title("Simulador de Tráfico Inteligente")
ventana.geometry("1200x650")
ventana.config(bg="#1e1e1e")

canvas = tk.Canvas(
    ventana,
    width=1200,
    height=650,
    bg="#2d2d2d",
    highlightthickness=0
)

canvas.pack()

canvas.create_rectangle(
    0,
    250,
    1200,
    450,
    fill="#3b3b3b",
    outline=""
)

for y in [300, 350, 400]:

    for i in range(0, 1200, 60):

        canvas.create_line(
            i,
            y,
            i + 30,
            y,
            fill="white",
            width=3
        )

estado_semaforo = "verde"

canvas.create_rectangle(
    560,
    120,
    610,
    250,
    fill="#1a1a1a"
)

luz_roja = canvas.create_oval(
    572,
    135,
    598,
    160,
    fill="gray"
)

luz_verde = canvas.create_oval(
    572,
    190,
    598,
    215,
    fill="green"
)

canvas.create_line(
    700,
    250,
    700,
    450,
    fill="white",
    width=5
)

canvas.create_text(
    600,
    40,
    text="SIMULADOR DE TRÁFICO MULTIHILO",
    fill="white",
    font=("Arial", 24, "bold")
)

canvas.create_text(
    600,
    80,
    text="Los carros se detienen en rojo y mantienen distancia",
    fill="#cccccc",
    font=("Arial", 13)
)

carros = []

def cambiar_semaforo():

    global estado_semaforo

    while True:

        # VERDE
        estado_semaforo = "verde"

        canvas.itemconfig(
            luz_verde,
            fill="green"
        )

        canvas.itemconfig(
            luz_roja,
            fill="gray"
        )

        time.sleep(6)

        estado_semaforo = "rojo"

        canvas.itemconfig(
            luz_verde,
            fill="gray"
        )

        canvas.itemconfig(
            luz_roja,
            fill="red"
        )

        time.sleep(6)


def mover_carro(carrito, velocidad):

    while True:

        coords = canvas.coords(carrito)

        x1 = coords[0]
        y1 = coords[1]
        x2 = coords[2]

        detener = False

        if estado_semaforo == "rojo":

            if x2 >= 650 and x2 <= 700:
                detener = True

        for otro_carro in carros:

            if otro_carro != carrito:

                coords_otro = canvas.coords(otro_carro)

                ox1 = coords_otro[0]
                oy1 = coords_otro[1]

                if abs(oy1 - y1) < 10:

                    if ox1 > x1 and ox1 - x2 < 50:
                        detener = True
                        break

        if not detener:

            canvas.move(
                carrito,
                velocidad,
                0
            )

        ventana.update()

        if x1 > 1200:

            nueva_y = random.choice([
                265,
                315,
                365
            ])

            canvas.coords(
                carrito,
                -120,
                nueva_y,
                -40,
                nueva_y + 35
            )

        time.sleep(0.03)

colores = [
    "#ff4444",
    "#00ccff",
    "#00ff88",
    "#ffaa00",
    "#ff66ff",
    "#ffffff"
]

carriles = [
    265,
    315,
    365
]

for i in range(10):

    carril = random.choice(carriles)

    carro = canvas.create_rectangle(
        -200 - (i * 150),
        carril,
        -120 - (i * 150),
        carril + 35,
        fill=random.choice(colores),
        outline="black",
        width=2
    )

    carros.append(carro)

threading.Thread(
    target=cambiar_semaforo,
    daemon=True
).start()

for carro in carros:

    velocidad = random.uniform(2, 5)

    threading.Thread(
        target=mover_carro,
        args=(carro, velocidad),
        daemon=True
    ).start()

ventana.mainloop()