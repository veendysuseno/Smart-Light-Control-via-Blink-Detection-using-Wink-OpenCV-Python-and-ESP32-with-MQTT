import cv2
import random
import time
from paho.mqtt import client as mqtt_client

# Load Haar cascades for face and eye detection
cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cascade_eye = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

# Initialize video capture
cap = cv2.VideoCapture(0)

# Set font for text display
font = cv2.FONT_HERSHEY_PLAIN
count = 0  # Initialize blink count
flag = False  # Flag to track blink state

# MQTT broker configuration
broker = 'broker.emqx.io'
port = 1883
topic = "htmtfunas/97921921312/test"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_id)
client.connect(broker, port)

# Main loop for face detection and blinking detection
while True:
    ret, frame = cap.read()  # Capture frame from the webcam
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    gray = cv2.bilateralFilter(gray, 5, 1, 1)  # Apply bilateral filter for smoothing

    # Detect faces in the image
    faces = cascade_face.detectMultiScale(gray, 1.3, 5, minSize=(200, 200))
    
    if len(faces) > 0:  # If at least one face is detected
        for (x, y, w, h) in faces:
            # Draw rectangle around the detected face
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3)

            # Define region of interest for eye detection
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            
            # Detect eyes within the detected face
            eyes = cascade_eye.detectMultiScale(roi_gray, 1.3, 5, minSize=(20, 20))
            eye_count = len(eyes)  # Count detected eyes
            print(eye_count)

            # Check if eyes are closed (blink detected)
            if eye_count == 0 and not flag:
                count += 1  # Increment blink count
                client.publish(topic, "Hello ESP32: " + str(count))  # Publish blink count to MQTT
                time.sleep(0.5)  # Delay to avoid multiple counts for a single blink
                flag = True  # Set flag to indicate blink detected
            if eye_count == 2:
                flag = False  # Reset flag when eyes are detected again

    # Display the blink count on the video frame
    cv2.putText(frame, "Blinking Eyes: " + str(count), (70, 70), font, 3, (0, 0, 255), 2)
    
    # Show the video frame with detections
    cv2.imshow('Face Detection', frame)

    # Break the loop if 'q' key is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the video capture and close windows after breaking the loop
cap.release()
cv2.destroyAllWindows()
