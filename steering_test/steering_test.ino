// This file is part of the OpenMV project.
// Copyright (c) 2013-2017 Ibrahim Abdelkader <iabdalkader@openmv.io> & Kwabena W. Agyeman <kwagyeman@openmv.io>
// This work is licensed under the MIT license, see the file LICENSE for details.
#include <Servo.h>

#define THROTTLE_SERVO_PIN 6
#define STEERING_SERVO_PIN 10

#define SERIAL_BUAD_RATE 19200

Servo steering_servo, throttle_servo;

int steering = 1580; // was the middle today => 99 which is very close to the 100 I have it set for
// 2300 - 1580 = 720
// 1580 - 700 = 880

void setup()
{
  Serial.begin(SERIAL_BUAD_RATE);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  if (!steering_servo.attached()) {
    steering_servo.attach(STEERING_SERVO_PIN, 700, 2300);
    Serial.print("steering attached ");
    Serial.println(steering_servo.attached());
  }

  steering_servo.writeMicroseconds(steering);
  delay(100);

  Serial.print("steering set to ");
  Serial.println(steering_servo.read());
  delay(100);

  digitalWrite(LED_BUILTIN, HIGH);

  if (!throttle_servo.attached()) {
    throttle_servo.attach(THROTTLE_SERVO_PIN);//, 1100, 2000);
    //  throttle_servo.attach(THROTTLE_SERVO_PIN, 1500, 2000);
    Serial.print("throttle attached ");
    Serial.println(throttle_servo.attached());
    delay(2000);
  }

  digitalWrite(LED_BUILTIN, HIGH);

  // zero
  throttle_servo.writeMicroseconds(1500);
  delay(100);

  // crawl forward for a second
  throttle_servo.writeMicroseconds(1592);
  delay(1000);

  // zero
  throttle_servo.writeMicroseconds(1500);
  delay(100);

  // set to backward
  throttle_servo.writeMicroseconds(1368);
  delay(100);

  // zero
  throttle_servo.writeMicroseconds(1500);
  delay(100);

  // crawl backward for a second
  throttle_servo.writeMicroseconds(1350);
  delay(1000);

  // zero and wait 8 seconds
  throttle_servo.writeMicroseconds(1500);
  delay(8000);

  steering += 4;

  digitalWrite(LED_BUILTIN, LOW);
}
