const int ENA_PIN = 9;
const int IN1_PIN = 4;
const int IN2_PIN = 5;

const int ENB_PIN = 10;
const int IN3_PIN = 6;
const int IN4_PIN = 7;

const int TRIGGER_PIN = 3;
const int ECHO_PIN = 2;

const int DISTANCE_THRESHOLD = 15; // Distancia de detección en centímetros

void setup() {
  // Configurar los pines como entradas o salidas
  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);

  pinMode(ENB_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);

  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Iniciar la comunicación serial
  Serial.begin(9600);
}

void loop() {
  // Leer la orden enviada desde Python
  if (Serial.available() > 0) {
    char orden = Serial.read();
    
    // Realizar la acción correspondiente según la orden recibida
    switch (orden) {
      case 'C':
        avanzar();
        break;
      case 'I':
        girarIzquierda();
        break;
      case 'D':
        girarDerecha();
        break;
    }
  }
  
  // Medir la distancia
  long duration, distance;
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2; // Calcular la distancia en centímetros
  
  // Tomar acciones según la distancia medida
  if (distance <= DISTANCE_THRESHOLD) {
    // Detener el carro
    detener();
    
    // Retroceder en diagonal durante 1.5 segundos
    retrocederDiagonal();
    
    // Enviar la orden de detener al código Python
    Serial.println("1");
  }
}

void avanzar() {
  // Configurar los pines para avanzar en línea recta
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENA_PIN, 100);

  digitalWrite(IN3_PIN, HIGH);
  digitalWrite(IN4_PIN, LOW);
  analogWrite(ENB_PIN, 100);
}

void girarIzquierda() {
  // Configurar los pines para girar a la izquierda
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENA_PIN, 100);

  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, HIGH);
  analogWrite(ENB_PIN, 100);
}

void girarDerecha() {
  // Configurar los pines para girar a la derecha
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENA_PIN, 100);

  digitalWrite(IN3_PIN, HIGH);
  digitalWrite(IN4_PIN, LOW);
  analogWrite(ENB_PIN, 100);
}

void detener() {
  // Configurar los pines para detener el carro
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENA_PIN, 0);

  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  analogWrite(ENB_PIN, 0);
}

void retrocederDiagonal() {
  // Configurar los pines para retroceder en diagonal
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENA_PIN, 100);

  digitalWrite(IN3_PIN, HIGH);
  digitalWrite(IN4_PIN, LOW);
  analogWrite(ENB_PIN, 100);

  delay(1500); // Retroceder en diagonal durante 1.5 segundos

  detener();
}
