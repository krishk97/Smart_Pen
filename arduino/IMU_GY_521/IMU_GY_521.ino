#include<Wire.h>

#define BUTTON 3
#define DEBOUNCE 15
#define BAUD 115200
#define DATASTREAMS 6
#define MAXSAMPLES 100

const int MPU=0x68; // I2C Address of IMU

int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;

volatile bool record = false;
volatile int startStop = -1;

//int samples = 0;
//int16_t data[MAXSAMPLES][DATASTREAMS];

void setup(){
  pinMode(BUTTON, INPUT_PULLUP); // Enable Pull-Up Resistor on Button
  attachInterrupt(digitalPinToInterrupt(BUTTON), recordISR, CHANGE); // Change Record when Button Pressed
  
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B); // Power Management Register
  Wire.write(0);  // Wake Up Sensor  
  Wire.endTransmission(true);
  Serial.begin(BAUD);
}
void loop(){
  if (startStop == 1) {
    Serial.println("{");
    startStop = -1;
  } else if (startStop == 0) {
    Serial.println("}");
    startStop = -1;
  }
  
  if (record) {
    Wire.beginTransmission(MPU);
    Wire.write(0x3B);  // First IMU Data Register
    Wire.endTransmission(false);
    Wire.requestFrom(MPU,12,true);  
    
    AcX=Wire.read()<<8|Wire.read();    
    AcY=Wire.read()<<8|Wire.read();  
    AcZ=Wire.read()<<8|Wire.read();  
    GyX=Wire.read()<<8|Wire.read();  
    GyY=Wire.read()<<8|Wire.read();  
    GyZ=Wire.read()<<8|Wire.read(); 

    Serial.print("[");
    Serial.print(AcX);
    Serial.print(", ");
    Serial.print(AcY);
    Serial.print(", ");
    Serial.print(AcZ);
    Serial.print(", ");
    Serial.print(GyX);
    Serial.print(", ");
    Serial.print(GyY);
    Serial.print(", ");
    Serial.print(GyZ);
    Serial.println("]");

     /*
    data[samples][0] = AcX;
    data[samples][1] = AcY;
    data[samples][2] = AcZ;
    data[samples][3] = GyX;
    data[samples][4] = GyY;
    data[samples][5] = GyZ;
    samples++;
    */
    delay(25);
  }
}
/*
void sendData() {
  for (int i=0; i < samples; i++) {
    for (int j=0; j < DATASTREAMS; j++) {
      Serial.println(data[i][j]);
    }
  }
  samples = 0;
}
*/

void recordISR() {
 static unsigned long last_interrupt_time_press = 0;
 unsigned long interrupt_time = millis();
 if (interrupt_time - last_interrupt_time_press > DEBOUNCE) // Debounce Button Presses
 {
   //record = !record; // Invert record 
   int but = !digitalRead(BUTTON);
   record = but;
   startStop = but;
   /*
   if (record) {
     Serial.println("{");
   } else {
    Serial.println("}")
   }
   */
 }
 last_interrupt_time_press = interrupt_time;
}
