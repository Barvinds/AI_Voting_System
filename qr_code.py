from flask import Flask, render_template, request, jsonify  # Import jsonify
import cv2
from pyzbar.pyzbar import decode
import xml.etree.ElementTree as ET
from twilio.rest import Client
import pyttsx3
from flask_cors import CORS
import face_verification

app = Flask(__name__)
CORS(app)


# Twilio credentials
account_sid = 'ACfbdad9fa3970ca314bf156193517cec9'
auth_token = '36c75595afc6847e45a65b3fa347a8c5'
twilio_phone_number = '+17163515756'
user_phone_number = '+918870666787'


expected_data = {
    "uid": "336294599969",
    "name": "Barvin",
    "gender": "M",
    "yob": "2003",
    "co": "S/O: Sasi Kumar",
    "house": "29",
    "street": "yadhavar north street",
    "vtc": "Vadakku Vallioor",
    "po": "Vallioor",
    "dist": "Tirunelveli",
    "subdist": "Radhapuram",
    "state": "Tamil Nadu",
    "pc": "627117",
    "dob": "2003-06-08"
}

def compare_with_expected_data(xml_data):
    try:
        root = ET.fromstring(xml_data)
        attributes = {}
        for key, value in root.attrib.items():
            attributes[key] = value

        if attributes == expected_data:
            return True
        else:
            return False
    except ET.ParseError:
        return False

def call_user_with_twilio():
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=user_phone_number,
        from_=twilio_phone_number,
        url='http://demo.twilio.com/docs/voice.xml'
    )
    print("Calling user...")

@app.route('/')
def index():
    return render_template('qr_verification.html')

details_verified_once = False  # Add this variable

@app.route('/scan', methods=['POST'])
def scan_qr():
    global details_verified_once  # Add this global declaration
    if request.method == 'POST':
        cap = cv2.VideoCapture(0)

        details_verified = False
        verification_status = "Not verified"

        engine = pyttsx3.init()

        while True:
            ret, frame = cap.read()

            decoded_objects = decode(frame)
            if decoded_objects:
                for obj in decoded_objects:
                    data = obj.data.decode('utf-8')
                    print("Scanned Data:", data)

                    if details_verified or details_verified_once:  # Check if already verified once
                        verification_status = "Duplicated verified"
                        print(verification_status)
                        engine.say("Details duplicated verified")
                        engine.runAndWait()
                        continue

                    if compare_with_expected_data(data):
                        print("Details verified.")
                        details_verified = True
                        details_verified_once = True  # Set the flag to True
                        verification_status = "Verified"
                        engine.say("Details verified")
                        engine.runAndWait()
                    else:
                        print("Not verified")
                        engine.say("Details not verified")
                        engine.runAndWait()

            cv2.imshow("QR Code Scanner", frame)

            if details_verified:
                cv2.waitKey(3000)
                break

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

        if not details_verified:
            call_user_with_twilio()   

        # Return JSON response
        return jsonify({"status": verification_status})

if __name__ == "__main__":
    app.run(debug=True)