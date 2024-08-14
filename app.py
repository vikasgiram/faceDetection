from flask import Flask, render_template, Response, jsonify
import cv2

app = Flask(__name__)

# Initialize the Haar Cascade face detector
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)

def detect_faces(frame):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    return faces

def draw_bounding_box(frame, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return frame

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            faces = detect_faces(frame)
            frame_with_boxes = draw_bounding_box(frame.copy(), faces)
            ret, buffer = cv2.imencode('.jpg', frame_with_boxes)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_photo', methods=['POST'])
def capture_photo():
    success, frame = video_capture.read()
    if success:
        faces = detect_faces(frame)
        if len(faces) == 1:
            # Get the coordinates of the first detected face
            (x, y, w, h) = faces[0]
            # Expand the bounding box to include some area around the face
            padding = int(0.5 * h)  # 50% of the height as padding
            x_start = max(x - padding, 0)
            y_start = max(y - padding, 0)
            x_end = min(x + w + padding, frame.shape[1])
            y_end = min(y + h + padding, frame.shape[0])

            # Crop the expanded region
            face_region = frame[y_start:y_end, x_start:x_end]
            # Resize the cropped region to a standard passport size (e.g., 200x200 pixels)
            passport_size_face = cv2.resize(face_region, (200, 200))
            # Save the passport-sized face image without the bounding box
            cv2.imwrite('passport_photo.jpg', passport_size_face)
            return jsonify(message="Photo captured and saved successfully!")
        elif len(faces) > 1:
            return jsonify(message="Multiple faces detected. Photo not captured."), 400
        else:
            return jsonify(message="No face detected. Photo not captured."), 400
    else:
        return jsonify(message="Failed to capture photo"), 500

if __name__ == '__main__':
    app.run(debug=True)
