import face_recognition
import cv2

# Load a sample picture and learn how to recognize it.
image = face_recognition.load_image_file("IMG20230831071517.jpg")
face_encodings = face_recognition.face_encodings(image)

if face_encodings:
    print("Face encoding successful!")
else:
    print("No face detected.")
