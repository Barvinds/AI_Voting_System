import face_recognition
import cv2
import numpy as np
import os
import math
import time
import cvzone
from ultralytics import YOLO
from twilio.rest import Client
import pyttsx3

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACfbdad9fa3970ca314bf156193517cec9'
TWILIO_AUTH_TOKEN = '36c75595afc6847e45a65b3fa347a8c5'
TWILIO_FROM_NUMBER = '+17163515756'
TWILIO_TO_NUMBER = '+918870666787'

# Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

known_face_encodings = []
known_face_names = []
dataset_folder = "E:/Projects/Smart_Voting_System/dataset"

for filename in os.listdir(dataset_folder):
    if filename.endswith(".jpeg") or filename.endswith(".png"):
        image_path = os.path.join(dataset_folder, filename)
        person_name = os.path.splitext(filename)[0]
        person_image = face_recognition.load_image_file(image_path)
        person_face_encoding = face_recognition.face_encodings(person_image)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(person_name)

confidence = 0.6
model = YOLO("best.pt")
classNames = ["fake", "real"]

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

prev_frame_time = 0
new_frame_time = 0

def make_twilio_call():
    call = client.calls.create(
        twiml='<Response><Say>Fake face detected. Please attend to the situation immediately.</Say></Response>',
        to=TWILIO_TO_NUMBER,
        from_=TWILIO_FROM_NUMBER
    )
    print("Twilio call status:", call.status)

def display_message_and_close(msg):
    print(msg)
    time.sleep(5)
    cap.release()
    cv2.destroyAllWindows()

engine = pyttsx3.init()
while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img, stream=True, verbose=False)
    face_names = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])

            if conf > confidence:
                if classNames[cls] == 'real':
                    color = (0, 255, 0)
                    engine.say("Real face verified")
                    engine.runAndWait()
                    display_message_and_close("Real face verified")
                else:
                    color = (0, 0, 255)
                    make_twilio_call()
                    display_message_and_close("Fake face verified")

                # Recognize faces
                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_name = "Unknown"
                for face_encoding in face_encodings:
                    # Compare the face with known faces
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    face_name = name

                # Display the results on the image
                cvzone.cornerRect(img, (x1, y1, w, h), colorC=color, colorR=color)
                cvzone.putTextRect(img, f'{face_name} - {classNames[cls].upper()} {int(conf*100)}%',
                                   (max(0, x1), max(35, y1)), scale=2, thickness=4, colorR=color,
                                   colorB=color)
                
    cv2.imshow("Image", img)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the webcam
cap.release()
cv2.destroyAllWindows()
