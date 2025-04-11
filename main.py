import cv2
import face_recognition
import serial
import time

# ==== Configuración Arduino ====
arduino = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)

# ==== Imagen de referencia ====
image = cv2.imread("Images/Choni.jpg")
face_loc = face_recognition.face_locations(image)[0]
face_image_encodings = face_recognition.face_encodings(image, known_face_locations=[face_loc])[0]
print("face_image_encodings:", face_image_encodings) # imprimir los valores en consola

# ==== Inicialización cámara ====
cap = cv2.VideoCapture(0)

# ==== Estado anterior ====
rostro_detectado_anteriormente = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    face_locations = face_recognition.face_locations(frame)  # Cambiar a "cnn" si se tiene dlib con CUDA    , model="cnn"

    if face_locations:
        for face_location in face_locations:
            face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
            result = face_recognition.compare_faces([face_image_encodings], face_frame_encodings)

            if result[0]:
                text = "Acceso Conocido"
                color = (0, 255, 0)

                if not rostro_detectado_anteriormente:
                    arduino.write(b'A')  # Encender LED solo una vez
                    rostro_detectado_anteriormente = True

            else:
                text = "Desconocido"
                color = (0, 0, 255)

                if rostro_detectado_anteriormente:
                    arduino.write(b'B')  # Apagar LED
                    rostro_detectado_anteriormente = False

            # Mostrar recuadro
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom), (right, bottom + 30), color, cv2.FILLED)
            cv2.putText(frame, text, (left + 6, bottom + 24), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

    else:
        # Si no hay rostros, apagar LED si estaba encendido
        if rostro_detectado_anteriormente:
            arduino.write(b'B')
            rostro_detectado_anteriormente = False

    # Mostrar frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
