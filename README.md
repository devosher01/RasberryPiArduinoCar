# Proyecto de Seguimiento de Colores con Python y Arduino

Este proyecto utiliza Python y Arduino para seguir objetos de diferentes colores. Utiliza la biblioteca OpenCV para el procesamiento de imágenes y la biblioteca serial para la comunicación con Arduino.

## Dependencias
- Python
- OpenCV
- numpy
- pySerial

## Cómo ejecutar el código
1. Asegúrate de tener instaladas todas las dependencias.
2. Conecta tu Arduino a tu computadora y ajusta el nombre del puerto en el código.
3. Ejecuta el script `script.py`.

## Descripción del código
El script `script.py` realiza las siguientes operaciones:
1. Captura imágenes de la cámara.
2. Filtra la imagen para mostrar solo objetos de un color específico (rojo, azul, verde, amarillo).
3. Identifica la ubicación del objeto de color en la imagen.
4. En función de la ubicación del objeto, envía un comando a Arduino para moverse hacia el objeto.
5. Si recibe un valor "1" de Arduino, pasa al siguiente color.

El código Arduino realiza las siguientes operaciones:
1. Lee la orden enviada desde Python y realiza la acción correspondiente (avanzar, girar a la izquierda, girar a la derecha).
2. Mide la distancia a los objetos y toma acciones si un objeto está demasiado cerca (detener el carro, retroceder en diagonal).
3. Envía la orden de detener al código Python si un objeto está demasiado cerca.

## Contribuciones
Las contribuciones a este proyecto son bienvenidas. Por favor, abre un problema o una solicitud de extracción si deseas contribuir.
