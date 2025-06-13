import cv2
import face_recognition
import serial
import time
import os

# ==== Configuración del puerto serie para comunicarse con Arduino ====
arduino = serial.Serial('COM10', 9600, timeout=1)
time.sleep(2)  # Esperar a que el Arduino inicie correctamente

# ==== Cargar múltiples imágenes de rostros conocidos ====
known_face_encodings = []  # Lista para guardar las codificaciones faciales
known_face_names = []      # Lista para guardar los nombres asociados a cada rostro

images_path = "Images"  # Carpeta donde están las imágenes de referencia

# Recorrer cada archivo en la carpeta de imágenes
for filename in os.listdir(images_path):
    if filename.endswith(('.jpg', '.png', '.jpeg')):  # Verifica que sea una imagen
        img_path = os.path.join(images_path, filename)
        image = face_recognition.load_image_file(img_path)
        face_locations = face_recognition.face_locations(image)

        if face_locations:  # Verifica que haya al menos un rostro en la imagen
            encoding = face_recognition.face_encodings(image, known_face_locations=face_locations)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(filename.split('.')[0])  # Guarda el nombre sin la extensión del archivo

print("Rostros cargados:", known_face_names)  # Mostrar en consola los nombres cargados

# ==== Inicialización de la cámara ====
cap = cv2.VideoCapture(0)

# Variable para controlar si ya se detectó un rostro antes (para no enviar señal repetida)
rostro_detectado_anteriormente = False

# ==== Bucle principal ====
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Si no se pudo capturar imagen, termina el bucle

    frame = cv2.flip(frame, 1)  # Voltea la imagen horizontalmente (como un espejo)

    # Detectar ubicaciones de rostros y sus codificaciones en el frame actual
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Analizar cada rostro detectado
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Desconocido"
        color = (0, 0, 255)  # Rojo por defecto

        if True in matches:
            match_index = matches.index(True)  # Obtener el índice del rostro que coincide
            name = known_face_names[match_index]
            color = (0, 255, 0)  # Verde si es conocido

            if not rostro_detectado_anteriormente:
                arduino.write(b'A')  # Enviar señal para encender LED
                rostro_detectado_anteriormente = True
        else:
            if rostro_detectado_anteriormente:
                arduino.write(b'B')  # Enviar señal para apagar LED
                rostro_detectado_anteriormente = False

        # Dibujar recuadro y nombre en el frame
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom), (right, bottom + 30), color, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom + 24), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

    # Si no se detectan rostros pero antes había uno, apagar LED
    if not face_locations and rostro_detectado_anteriormente:
        arduino.write(b'B')
        rostro_detectado_anteriormente = False

    # Mostrar imagen en una ventana
    cv2.imshow("Detección de Rostros con IA", frame)
    if cv2.waitKey(1) == 27:  # Presionar ESC para salir
        break

# ==== Limpieza final ====
cap.release()
cv2.destroyAllWindows()