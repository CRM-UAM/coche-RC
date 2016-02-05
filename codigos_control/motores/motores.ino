
#include <Servo.h>

#define PIN_SERVO 12
#define PIN_EN_A 5
#define PIN_EN_B 3
#define PIN_DIR1_A 11
#define PIN_DIR2_A 10
#define PIN_DIR1_B 9
#define PIN_DIR2_B 8
#define LED 13
#define MAX_DER_DIR 55
#define MAX_IZQ_DIR 150

Servo direccion;

/**
 * Funcion para controlar la traccion delantera
 * parametros:
 *  - vel: [-100,100], regula la velocidad del motor siendo -100 maxima velocidad marcha atras y 0 parado (motor libre).
 */
void motorDelantero(long vel){
  if(vel<-100)vel=-100;
  if(vel>100)vel=100;
  if(vel==0){
    digitalWrite(PIN_DIR1_A,LOW);
    digitalWrite(PIN_DIR2_A,LOW);
    analogWrite(PIN_EN_A, 0);
    return;
  }
  if(vel < 0){
    vel=-vel;
    digitalWrite(PIN_DIR1_A,LOW);
    digitalWrite(PIN_DIR2_A,HIGH);
  }else{
    digitalWrite(PIN_DIR1_A,HIGH);
    digitalWrite(PIN_DIR2_A,LOW);
  }
  long v=map(vel,-100,100,0, 255);
  analogWrite(PIN_EN_A, v);
}
/**
 * Funcion para controlar la traccion trasera
 * parametros:
 *  - vel: [-100,100], regula la velocidad del motor siendo -100 maxima velocidad marcha atras y 0 parado (motor libre).
 */
void motorTrasero(long vel){
  if(vel<-100)vel=-100;
  if(vel>100)vel=100;
  if(vel==0){
    digitalWrite(PIN_DIR1_B,LOW);
    digitalWrite(PIN_DIR2_B,LOW);
    analogWrite(PIN_EN_B, 0);
    return;
  }
  if(vel < 0){
    vel=-vel;
    digitalWrite(PIN_DIR1_B,LOW);
    digitalWrite(PIN_DIR2_B,HIGH);
  }else{
    digitalWrite(PIN_DIR1_B,HIGH);
    digitalWrite(PIN_DIR2_B,LOW);
  }
  long v=map(vel,-100,100,0,255);
  analogWrite(PIN_EN_B, v); 
}

/**
 * Controla la direccion del coche.
 * parametro:
 *  -ang: [-90,90] , siendo -90 el angulo máximo de giro a la derecha y +90 hacia la izquierda.
 */
void setDir(int ang){
  if(ang<-90)ang=-90;
  if(ang>90)ang=90;
  int a=map(ang,-90,90,MAX_DER_DIR,MAX_IZQ_DIR);
  direccion.write(a);
}


void setup() {
  delay(2000);
  pinMode(PIN_SERVO,OUTPUT);
  pinMode(PIN_EN_A,OUTPUT);
  pinMode(PIN_EN_B,OUTPUT);
  pinMode(PIN_DIR1_A,OUTPUT);
  pinMode(PIN_DIR2_A,OUTPUT);
  pinMode(PIN_DIR1_B,OUTPUT);
  pinMode(PIN_DIR2_B,OUTPUT);
  direccion.attach(PIN_SERVO);

}





void loop() {
  /*direccion.write(50);
  delay(1000);
  direccion.write(160);
  delay(1000);
  direccion.write((MAX_DER_DIR+MAX_IZQ_DIR)/2);
  delay(2000);
  */ 
  direccion.write((MAX_IZQ_DIR+MAX_DER_DIR)/2);
  motorDelantero(10);
  motorTrasero(20);
  delay(2000);
  motorDelantero(0);
  motorTrasero(0);
  delay(1000);
  
  motorDelantero(-10);
  motorTrasero(-20);
  delay(2000);
  motorDelantero(0);
  motorTrasero(0);
  delay(1000000);
  

}
