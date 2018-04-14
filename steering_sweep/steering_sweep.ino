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
int i = 0;
int steering = 98;
int middle = 1580;

void setup()
{
  Serial.begin(SERIAL_BUAD_RATE);
  pinMode(LED_BUILTIN, OUTPUT);
  // defaults: min=544, max =2400 (mid would be 1472)

  // mid-point between 1100-2000 is 1550.

  // mid-point between 1160-2000 is 1580.
//  steering_servo.attach(STEERING_SERVO_PIN, 1160, 2000); 


  // mid-point between 1276 - 1884 is 1580. 
  // 1276 corresponded to 69 and 1884 corresponded to 110
//  steering_servo.attach(STEERING_SERVO_PIN, 1276, 1884); // latest
  
  //  throttle_servo.attach(THROTTLE_SERVO_PIN);//, 1100, 2000);

  

  delay(100);
  int j = 0;
  for (j = 0; j < 10; j++) {
    steering_servo.writeMicroseconds(middle);
    delay(100);

    // 700-2300: max=132, min=70
    // 1100-1900: max=130, min=70
    
    for (i = middle; i <= 1884; i += 4) {
      //    steering_servo.write(i);
      steering_servo.writeMicroseconds(i);
      Serial.print(i);
      Serial.print(" us = ");
      Serial.println(steering_servo.read());
      delay(50);
    }

    for (i = middle; i >= 1276; i -= 4) {
      //    steering_servo.write(i);
      steering_servo.writeMicroseconds(i);
      Serial.print(i);
      Serial.print(" us = ");
      Serial.println(steering_servo.read());
      delay(50);
    }

  }
  //1880, 2100
  // 1270, 1080

  //  for (i = 100; i >= 0; i--) {
  //    steering_servo.write(i);
  //    Serial.println(steering_servo.read());
  //    delay(500);
  //  }

  steering_servo.writeMicroseconds(1600);
  delay(100);

  steering_servo.detach();
  //  throttle_servo.detach();

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



  //  for (i = 0; i <= 180; i++) {
  //    Serial.println(20 - (easein(i / 180.0) * 9.0));
  //  }

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
