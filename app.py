from flask import Flask, jsonify, make_response
import cv2
import base64
import numpy as np

app = Flask(__name__)

# Initialize the Haar Cascade face detector
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)

def detect_bounding_box(frame):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    return faces

@app.route('/', methods=['GET'])
def capture_photo():
    success, frame = video_capture.read()
    if success:
        faces = detect_bounding_box(frame)
        if len(faces) == 1:
            (x, y, w, h) = faces[0]
            padding = int(0.5 * h)
            x_start = max(x - padding, 0)
            y_start = max(y - padding, 0)
            x_end = min(x + w + padding, frame.shape[1])
            y_end = min(y + h + padding, frame.shape[0])
            
            face_region = frame[y_start:y_end, x_start:x_end]
            passport_size_face = cv2.resize(face_region, (200, 200))
            
            # Encode the image to a buffer
            _, img_encoded = cv2.imencode('.jpg', passport_size_face)
            img_bytes = img_encoded.tobytes()
            
            # Convert the bytes to a Base64 string
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            # Create a JSON response with the Base64 string
            response = {
                'status': 'success',
                'image': img_base64
            }
            return jsonify(response), 200
        
        elif len(faces) > 1:
            return jsonify(message="Multiple faces detected. Photo not captured."), 400
        else:
            return jsonify(message="No face detected. Photo not captured."), 400
    else:
        return jsonify(message="Failed to capture photo"), 500

if __name__ == '__main__':
    app.run()
