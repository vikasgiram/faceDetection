from flask import Flask, jsonify, request
import base64
import cv2
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize the Haar Cascade face detector
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_bounding_box(frame):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    return faces

@app.route('/')
def index():
    return "Welcome to the Face Detection API Please make post request with base64 image string"

@app.route('/', methods=['POST'])
def process_image():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)  # Get the client's IP address
    data = request.get_json()

    # Print the access to the console
    print(f"--------------------API accessed by {client_ip}--------------------")
    
    if 'image' not in data:
        print(f"--------------------Request from {client_ip} did not include an image.--------------------")
        return jsonify(message="Image data not provided"), 400

    try:
        # Decode the base64 image
        img_data = base64.b64decode(data['image'])
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

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

            # Encode the image to Base64
            _, img_encoded = cv2.imencode('.jpg', passport_size_face)
            img_bytes = img_encoded.tobytes()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            # Print the successful result to the console
            print(f"--------------------Face detected and processed sucess for {client_ip}.--------------------")
            
            response = {
                'status': 'success',
                'image': img_base64
            }
            return jsonify(response), 200
        
        elif len(faces) > 1:
            print(f"Multiple faces detected for {client_ip}.")
            return jsonify(message="Multiple faces detected. Photo not processed."), 400
        else:
            print(f"No face detected for {client_ip}.")
            return jsonify(message="No face detected. Photo not processed."), 400

    except Exception as e:
        print(f"Error processing image from {client_ip}: {str(e)}")
        return jsonify(message="Error processing image"), 500

if __name__ == '__main__':
    app.run()
