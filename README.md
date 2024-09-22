# Smart Light Control via Blink Detection using Wink OpenCV, Python, and ESP32 with MQTT

## Project Overview

This project integrates face detection using OpenCV in Python and an ESP32 microcontroller that reacts to MQTT messages. When a face is detected and the user blinks, a message is sent to the ESP32 to control a relay.

## Requirements

- Python 3.x
- OpenCV (opencv-python==4.5.5.64)
- Paho MQTT library (paho-mqtt==1.6.1)
- ESP32 with Wi-Fi capabilities
- Arduino IDE or code editors (e.g. VS Code Studio)

## Explanation:

- opencv-python==4.5.5.64: A specific version of OpenCV for consistent behavior across environments.
- paho-mqtt==1.6.1: A specific version of the Paho MQTT client.

You can install these specific versions using:

```bash
pip install -r requirements.txt

```

## Code Structure

1. **main.py**:

- This script captures video from the webcam, detects faces and eyes, and publishes messages to an MQTT broker when a blink is detected.

```python
import cv2
import random
from paho.mqtt import client as mqtt_client
import time

# MQTT Configuration
broker = 'broker.emqx.io'
port = 1883
topic = "htmtfunas/97921921312/tes"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_id)
client.connect(broker, port)

# Cascade Classifiers
cascade_wajah = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cascade_mata = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
cap = cv2.VideoCapture(0)

count = 0
flag = False
font = cv2.FONT_HERSHEY_PLAIN

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 5, 1, 1)
    faces = cascade_wajah.detectMultiScale(gray, 1.3, 5, minSize=(200, 200))

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)

            roi_gray = gray[y:y + h, x:x + w]
            mata = cascade_mata.detectMultiScale(roi_gray, 1.3, 5, minSize=(20, 20))
            jumlah = len(mata)

            if jumlah == 0 and not flag:
                count += 1
                client.publish(topic, f"Hello Esp32: {count}")
                time.sleep(0.5)
                flag = True
            if jumlah == 2:
                flag = False

    cv2.putText(frame, f"Mata Berkedip: {count}", (70, 70), font, 3, (0, 0, 255), 2)
    cv2.imshow('Face Detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break

```

2. **publish.py**:

- A simple script to publish a message to the MQTT broker.

```python
import random
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "htmtfunas/97921921312/tes"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_id)
client.connect(broker, port)

client.publish(topic, "hello world")

```

3. **esp32.ino**:

- Arduino code for the ESP32 to connect to Wi-Fi and listen for MQTT messages to control a relay.

```cpp
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Your_SSID";
const char* password = "Your_PASSWORD";
const char* mqtt_server = "broker.emqx.io";

WiFiClient espClient;
PubSubClient client(espClient);
#define relay 5

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("WiFi connected");
}

int count = 0;
void callback(char* topic, byte* payload, unsigned int length) {
    count++;
    if (count == 1) {
        digitalWrite(relay, HIGH);
    } else if (count == 2) {
        digitalWrite(relay, LOW);
        count = 0;
    }
}

void reconnect() {
    while (!client.connected()) {
        String clientId = "ESP8266Client-";
        clientId += String(random(0xffff), HEX);
        if (client.connect(clientId.c_str())) {
            client.subscribe("htmtfunas/97921921312/tes");
        }
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(relay, OUTPUT);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
}

```

## Usage

1. Run main.py to start the face detection and MQTT publishing.
2. Upload the esp32.ino code to your ESP32 using the Arduino IDE.
3. Ensure your ESP32 is connected to the same Wi-Fi network and configured correctly.

## Notes:

- Modify the SSID and password in the esp32.ino file as needed.
- You can stop the face detection by pressing 'q'.

## Conclusion

This project showcases how to combine computer vision with IoT devices using MQTT for communication. You can extend the functionality further by adding more sensors or integrating additional features.
