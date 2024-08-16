
# Face Detection API

This repository contains a Flask-based API that detects faces in images. The API accepts an image in Base64 format, processes it using OpenCV, and returns the processed image with the detected face (if any) in Base64 format.

## Features

- **Face Detection**: The API can detect a single face in the provided image and return the processed image containing only the detected face.
- **Base64 Encoding**: Both the input and output images are in Base64 format, making it easy to integrate with web applications.
- **Console Logging**: The API logs the client IP address and the result of the face detection process directly to the server console.

## How It Works

1. The client sends a POST request with a Base64-encoded image to the `https://facedetection-hnz5.onrender.com` endpoint.
2. The API detects any faces in the image using OpenCV's Haar Cascade Classifier.
3. If exactly one face is detected, the face is cropped and resized to passport size (200x200 pixels).
4. The processed image is returned as a Base64-encoded string in the JSON response.
5. The API prints logs to the console showing who accessed the API and the result of the face detection.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- Flask
- OpenCV
- NumPy

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vikasgiram/faceDetection.git
   cd faceDetection
   ```

2. **Install Dependencies**:
   Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

   The API will be running at `http://localhost:5000`.

### Deployment

The API is deployed and accessible via Render. You can use the following endpoint to access the live API:

- **Live Endpoint**: `https://facedetection-hnz5.onrender.com/`

### API Usage

#### Request

- **Endpoint**: `/`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**: JSON containing a Base64-encoded image.

Example Request Body:

```json
{
  "image": "<Base64-encoded-image>"
}
```

#### Response

- **Success (200)**: If a single face is detected, the response will contain the processed image in Base64 format.
  ```json
  {
    "status": "success",
    "image": "<Base64-encoded-passport-photo>"
  }
  ```
- **Failure (400)**: If no face or multiple faces are detected, or if the image is not provided.
  ```json
  {
    "message": "No face detected. Photo not processed."
  }
  ```
  ```json
  {
    "message": "Multiple faces detected. Photo not processed."
  }
  ```
- **Error (500)**: If there is an issue processing the image.
  ```json
  {
    "message": "Error processing image"
  }
  ```

### Example Usage in Python

```python
import requests
import base64

# Encode image to Base64
with open('test_image.jpg', 'rb') as img_file:
    base64_image = base64.b64encode(img_file.read()).decode('utf-8')

# Send the request
url = 'https://facedetection-hnz5.onrender.com/'
data = {
    'image': base64_image
}
response = requests.post(url, json=data)

# Print the response
print(response.json())
```

### Example Usage in Angular

You can integrate the API into an Angular application using the `HttpClient` module. Here's an example:

```typescript
import { HttpClient } from '@angular/common/http';

export class FaceDetectionService {
  private apiUrl = 'https://facedetection-hnz5.onrender.com/process_image';

  constructor(private http: HttpClient) {}

  processImage(base64Image: string) {
    const payload = { image: base64Image };
    return this.http.post(this.apiUrl, payload);
  }
}
```

### Logging

- The API logs the following information to the server console:
  - IP address of the client making the request.
  - Whether a face was detected, multiple faces were detected, or no faces were detected.
  - Any errors that occur during processing.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
