#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);

  while (!Serial)
    delay(10);

  Serial.println("Iniciando MPU6050...");

  if (!mpu.begin()) {
    Serial.println("No se encontró el MPU6050");
    while (1) {
      delay(10);
    }
  }

  Serial.println("MPU6050 conectado correctamente");
}

void loop() {
  sensors_event_t a, g, temp;

  mpu.getEvent(&a, &g, &temp);

  Serial.print("Aceleración X: ");
  Serial.print(a.acceleration.x);
  Serial.print("  Y: ");
  Serial.print(a.acceleration.y);
  Serial.print("  Z: ");
  Serial.println(a.acceleration.z);

  delay(500);
}
