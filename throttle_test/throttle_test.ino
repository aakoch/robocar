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
int i = 1580; // "beeped" but wheels didn't move at 1550, 1560, 1570, 1580 - wheels moved at 1590 - now 1610 (floor was 1620)
// backwards - 1400??
// wheels going backwards at 1399
// "beeped" but wheels didn't move at 1449, 1440, 1430, 1422, 1402
int backward_delay = 500;

void setup()
{
  Serial.begin(SERIAL_BUAD_RATE);
  pinMode(LED_BUILTIN, OUTPUT);

  steering_servo.attach(STEERING_SERVO_PIN, 700, 2300);
  Serial.print("steering attached ");
  Serial.println(steering_servo.attached());
  steering_servo.write(100);
  Serial.print("steering set to ");
  Serial.println(steering_servo.read());
  delay(100);
  steering_servo.detach();
  delay(100);

}

//void(* resetFunc) (void) = 0;

void loop()
{
  last_milliseconds = millis();
  digitalWrite(LED_BUILTIN, HIGH);

//THROTTLE_SERVO_MIN_US = 1500
//THROTTLE_SERVO_MAX_US = 2000
//
//# Tweak these values for your robocar.
//STEERING_SERVO_MIN_US = 700
//STEERING_SERVO_MAX_US = 2300
// defaults: 544, 2400
if (!throttle_servo.attached()) {
  throttle_servo.attach(THROTTLE_SERVO_PIN);//, 1100, 2000);
//  throttle_servo.attach(THROTTLE_SERVO_PIN, 1500, 2000);
  Serial.print("throttle attached ");
  Serial.println(throttle_servo.attached());
  delay(2000);
}

  digitalWrite(LED_BUILTIN, LOW);
  throttle_servo.writeMicroseconds(1500);
  delay(100);
  digitalWrite(LED_BUILTIN, HIGH);
  throttle_servo.writeMicroseconds(1366);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  throttle_servo.writeMicroseconds(1500);
  delay(100);
// 1385, 
  for (i = 1378; i >= 1376; i -= 2) {

    Serial.print(backward_delay);
    Serial.print(", ");
    Serial.println(i);

//    throttle_servo.write(i);
    throttle_servo.writeMicroseconds(i);
    delay(100);// 500 first time only?
  }

//  backward_delay = random(300, 700);

  throttle_servo.writeMicroseconds(1500);

  delay(100);

  //  1398 on table, floor was 1402?!
  
  for (i = 1590; i <= 1592; i += 1) {

    Serial.print(throttle_servo.read());
    Serial.print(" => ");
    Serial.println(i);

    throttle_servo.writeMicroseconds(i);
    delay(100);
  }

  throttle_servo.writeMicroseconds(1500);
  delay(100);

//  throttle_servo.detach();
//  delay(500);

  digitalWrite(LED_BUILTIN, LOW);
}
