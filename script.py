import serial
import cv2
import numpy as np

# Función para filtrar el color especificado y eliminar el ruido
def filtrar_color(frame, color_bajo, color_alto):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, color_bajo, color_alto)
    
    # Eliminar el ruido utilizando operaciones morfológicas
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Encontrar los contornos de los objetos filtrados
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Encontrar el contorno más grande (mayor área)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Crear una máscara solo para el contorno más grande
        mask_largest = np.zeros_like(mask)
        cv2.drawContours(mask_largest, [largest_contour], -1, 255, cv2.FILLED)
        
        # Filtrar el color en el marco original usando la máscara del contorno más grande
        frame_filtrado = cv2.bitwise_and(frame, frame, mask=mask_largest)
    else:
        frame_filtrado = np.zeros_like(frame)
        
    return frame_filtrado

# Configuración de la cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Arreglo de colores a filtrar (rojo, azul, verde, amarillo)
colores = [
    (np.array([135, 113, 121], np.uint8), np.array([179, 255, 255], np.uint8)),  # Rojo
    (np.array([100, 100, 20], np.uint8), np.array([125, 255, 255], np.uint8)),  # Azul
    (np.array([45, 83, 92], np.uint8), np.array([100, 255, 255], np.uint8)),  # Verde
    (np.array([15, 100, 20], np.uint8), np.array([45, 255, 255], np.uint8))  # Amarillo
]

# Configuración del puerto serie (ajusta el nombre del puerto según tu configuración)
puerto_serie = serial.Serial("COM7", 9600)
# Definir los valores numéricos correspondientes a cada color
valores_numericos = {
    "rojo": 0,
    "azul": 1,
    "verde": 2,
    "amarillo": 3
}

for color_bajo, color_alto in colores:
    # Mostrar el nombre del color
    color_name = ""
    if color_bajo[0] <= 10 and color_alto[0] >= 170:
        color_name = "Rojo"
    elif color_bajo[0] >= 90 and color_alto[0] <= 130:
        color_name = "Azul"
    elif color_bajo[0] >= 35 and color_alto[0] <= 75:
        color_name = "Verde"
    elif color_bajo[0] >= 15 and color_alto[0] <= 45:
        color_name = "Amarillo"
    print("Filtrando color:", color_name)

    # Filtrar y mostrar el color
    while True:
        ret, frame = cap.read()

        if ret:
            # Filtrar el color especificado y eliminar el ruido
            frame_filtrado = filtrar_color(frame, color_bajo, color_alto)

            # Obtener ubicación del objeto
            contours, _ = cv2.findContours(cv2.cvtColor(frame_filtrado, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                x, _, w, _ = cv2.boundingRect(contours[0])
                centro_objeto = x + w // 2
                pantalla_centro = cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2
                if centro_objeto < pantalla_centro - 50:
                    print("El objeto está a la izquierda")
                    puerto_serie.write(b'I')  # Enviar orden de girar a la izquierda
                elif centro_objeto > pantalla_centro + 50:
                    print("El objeto está a la derecha")
                    puerto_serie.write(b'D')  # Enviar orden de girar a la derecha
                else:
                    print("El objeto está en el centro")
                    puerto_serie.write(b'C')  # Enviar orden de avanzar recto

            # Mostrar el resultado
            cv2.imshow('frame', frame_filtrado)
            cv2.waitKey(1)

            # Leer el valor enviado por Arduino
            if puerto_serie.in_waiting > 0:
                value = puerto_serie.readline().decode().strip()
                print('Arduino, ', value)
                if value == "1":
                    break

cap.release()
cv2.destroyAllWindows()
puerto_serie.close()
