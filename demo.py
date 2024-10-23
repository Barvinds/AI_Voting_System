from flask import Flask, jsonify, render_template, Response
import cv2
import numpy as np
import face_recognition
from ultralytics import YOLO
import pyttsx3
import os
from twilio.rest import Client
from flask_cors import CORS
import math
import time
from scipy import stats

app = Flask(__name__)
CORS(app)

global_status = "not_verified"

# Twilio credentials and client setup
TWILIO_ACCOUNT_SID = 'ACfbdad9fa3970ca314bf156193517cec9'
TWILIO_AUTH_TOKEN = '36c75595afc6847e45a65b3fa347a8c5'
TWILIO_FROM_NUMBER = '+17163515756'
TWILIO_TO_NUMBER = '+918870666787'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

global_status = "not_verified"

# Loading known face encodings
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

# Model and voice engine initialization
confidence = 0.6 
model = YOLO("best.pt")
classNames = ["fake", "real"]
engine = pyttsx3.init()

# Global status
global_status = "not verified"

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

def gen():
    global global_status
    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        results = model(img, stream=True, verbose=False)
        face_names = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])

                if conf > confidence:
                    if classNames[cls] == 'real':
                        engine.say("Real face verified")
                        engine.runAndWait()
                        global_status = "verified"
                        break
                    else:
                        make_twilio_call()
                        display_message_and_close("Fake face detected")
                        break

                    # Display the result
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(img, f'{global_status.upper()} {conf * 100:.0f}%', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.imshow("Face Scanner", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('face_verification.html')

@app.route('/video_feed', methods=['POST'])
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/verify_face', methods=['POST'])
def verify_face_status():
    global global_status
    return jsonify({"status": global_status})

if __name__ == '__main__':
    app.run(debug=True)
