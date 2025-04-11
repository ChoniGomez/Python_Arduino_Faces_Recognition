void setup() {
  pinMode(13, OUTPUT);         // Configuramos el pin 13 como salida
  Serial.begin(9600);          // Iniciamos la comunicación serial a 9600 baudios
}

void loop() {
  if (Serial.available() > 0) {  // Si hay datos disponibles en el puerto serie
    char dato = Serial.read();   // Leemos el dato recibido
    Serial.println(dato);
    if (dato == 'A') {
      digitalWrite(13, HIGH);    // Encendemos el LED (pin 13)
    } 
    else if (dato == 'B') {
      digitalWrite(13, LOW);     // Apagamos el LED
    }
  }
}
