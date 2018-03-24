//char incomingByte[16] = {};


// Example 2 - Receive with an end-marker

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;

void setup() {
  Serial.begin(19200);
    Serial.println("<Arduino is ready>");
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
    char endMarker = '\n';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
      digitalWrite(LED_BUILTIN, HIGH);
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
    digitalWrite(LED_BUILTIN, LOW);
}

void showNewData() {
//    if (newData == true) {
    digitalWrite(LED_BUILTIN, HIGH);
        Serial.print("This just in ... ");
        Serial.println(receivedChars);
//        newData = false;
    digitalWrite(LED_BUILTIN, LOW);
    delay(2000);
//    }
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
