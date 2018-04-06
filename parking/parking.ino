// This file is part of the OpenMV project.
// Copyright (c) 2013-2017 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
// This work is licensed under the MIT license, see the file LICENSE for details.


#include <Servo.h>

#define SERIAL_RX_PIN 0
#define SERIAL_TX_PIN 1
#define THROTTLE_SERVO_PIN 6
#define STEERING_SERVO_PIN 10
#define RC_THROTTLE_SERVO_PIN 11
#define RC_STEERING_SERVO_PIN 5

#define SERIAL_BUAD_RATE 19200

#define RC_THROTTLE_SERVO_REFRESH_RATE 20000UL // in us
#define SERIAL_THROTTLE_SERVO_REFRESH_RATE 1000000UL // in us
#define RC_THROTTLE_DEAD_ZONE_MIN 1400UL // in us
#define RC_THROTTLE_DEAD_ZONE_MAX 1600UL // in us

#define RC_STEERING_SERVO_REFRESH_RATE 20000UL // in us
#define SERIAL_STEERING_SERVO_REFRESH_RATE 1000000UL // in us
#define RC_STEERING_DEAD_ZONE_MIN 1400UL // in us
#define RC_STEERING_DEAD_ZONE_MAX 1600UL // in us

Servo steering_servo, throttle_servo;

unsigned long last_milliseconds;
float i = 0;
int steering = 98;

void setup()
{
  Serial.begin(SERIAL_BUAD_RATE);
  pinMode(LED_BUILTIN, OUTPUT);
  steering_servo.attach(STEERING_SERVO_PIN, 700, 2300);
  throttle_servo.attach(THROTTLE_SERVO_PIN);//, 1100, 2000);
  delay(1000);
  
  steering_servo.write(100);
  
  throttle_servo.writeMicroseconds(1500);
  delay(200);
  
  throttle_servo.writeMicroseconds(1592);
  delay(2000);

  
  throttle_servo.writeMicroseconds(1500);
  delay(800);

  steering_servo.write(0);
  throttle_servo.writeMicroseconds(1366);
  delay(200);
  
  throttle_servo.writeMicroseconds(1500);
  delay(200);
  
  throttle_servo.writeMicroseconds(1368);

//  for (i = 1; i <= 180; i += 1) {
//    steering_servo.write(i);
//    delay(10);
//    Serial.println(sin(float(i / 180.0)));
//  }
  
  for (i = 0; i <= 180; i++) {
    steering_servo.write(ease(float(i/180.0)) * 180);
    delay(18 - (ease(i / 180.0) * 9.0));
  
  }
  delay(20);

  steering_servo.write(100);
  throttle_servo.writeMicroseconds(1500);
  delay(200);

  steering_servo.detach();
  throttle_servo.detach();
}

float easein(float t) {
  return 2.0f * square(t);
}

float ease(float t) {

    float sqt = t * t;
    return sqt / (2.0f * (sqt - t) + 1.0f);
 }


void loop()
{

  for (i = 0; i <= 180; i++) {
    Serial.println(20 - (easein(i / 180.0) * 9.0));
  }
  
//  digitalWrite(LED_BUILTIN, LOW);
//  throttle_servo.writeMicroseconds(1500);
//  delay(100);
//
//  throttle_servo.writeMicroseconds(1376);
//  delay(1000);
//
//  throttle_servo.writeMicroseconds(1500);
//  delay(100);
//  throttle_servo.writeMicroseconds(1592);
//  delay(1000);
//  throttle_servo.writeMicroseconds(1500);
//  delay(8000);
//
//  digitalWrite(LED_BUILTIN, LOW);
}
