//char incomingByte[16] = {};


// Example 2 - Receive with an end-marker

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
const int endMarker = '\n';

char serial_buffer[16] = {};

boolean newData = false;
unsigned long serial_throttle_servo_pulse_length_tmp, serial_steering_servo_pulse_length_tmp;

void setup() {
  Serial.begin(19200);
  Serial.println("<Arduino is ready - expecting \\n as delimiter>");
}

void loop() {
  recvWithEndMarker();
  showNewData();

  //    digitalWrite(LED_BUILTIN, HIGH);
  //    delay(150);
  //    digitalWrite(LED_BUILTIN, LOW);
  //    delay(200);
}

void recvWithEndMarker() {
  static byte ndx = 0;
  int rc;

  while (Serial.available() > 0 && newData == false) {
    digitalWrite(LED_BUILTIN, HIGH);

    
    int c = Serial.read();
    memmove(serial_buffer, serial_buffer + 1, sizeof(serial_buffer) - 2);
    serial_buffer[sizeof(serial_buffer) - 2] = c;


    if (c == endMarker) {


      //      if (sscanf(serial_buffer, "{%lu,%lu}", &serial_throttle_servo_pulse_length_tmp, &serial_steering_servo_pulse_length_tmp) == 2) {
      //
      //      }


      //      receivedChars[ndx] = '\0'; // terminate the string
      //      ndx = 0;
      newData = true;
    }
    else {
      //      receivedChars[ndx] = rc;
      //      ndx++;
      //      if (ndx >= numChars) {
      //        ndx = numChars - 1;
      //      }
    }
  }
  digitalWrite(LED_BUILTIN, LOW);
}

void showNewData() {
  if (newData == true) {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print("This just in ... ");
    //    if (serial_throttle_servo_pulse_length_tmp) {
    //      Serial.println(serial_throttle_servo_pulse_length_tmp);
    //    }
    //    else
    Serial.println(serial_buffer);
    newData = false;
    digitalWrite(LED_BUILTIN, LOW);
    //    delay(2000);
  }
}

//
//void loop() {
//  // send data only when you receive data:
//  if (Serial.available()) {
//
//    digitalWrite(LED_BUILTIN, (digitalRead(LED_BUILTIN) == HIGH) ? LOW : HIGH);
//
//    // read the incoming byte:
//    incomingByte = Serial.readStringUntil('\r');
//
//    // say what you got:
//    Serial.print("I received: " + incomingByte);
//  }
//}
