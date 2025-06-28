# 🎓 Face Recognition Attendance System

This project is a real-time face recognition-based attendance system built using Python, OpenCV, and the `face_recognition` library. It uses a webcam to identify faces from a preloaded dataset and automatically marks attendance in a CSV file.

---

## Screenshot
![Screenshot 2025-06-28 012620](https://github.com/user-attachments/assets/39289aa0-c73c-4649-b852-b3c8edb25d44)

---
## 🛠️ Features

- Real-time face detection and recognition using webcam
- Automatic attendance marking with timestamp
- Ignores duplicate entries within a short time window (3 seconds)
- Simple CSV-based attendance logging
- Easy to add new students (just drop an image in the folder)

---
## Install Dependencies
  - step: Install the main dependencies
  command: |
    ```
    pip install opencv-python numpy face_recognition
    ```

- step: If you face issues with face_recognition (due to dlib), install cmake and dlib manually
  windows: 
    ```
    pip install cmake
    pip install dlib
    pip install face_recognition
    ```
  linux: 
    ```
    sudo apt-get install cmake
    sudo apt-get install libboost-all-dev
    pip install dlib
    pip install face_recognition
    ```
  note :
    - 💡 On Windows, you may also need to install Visual C++ Build Tools from:
    - https://visualstudio.microsoft.com/visual-cpp-build-tools/

---
## Add Student Images
  - Place clear front-facing images in the Students/ folder.
  - File names (excluding extension) should match the student's name (e.g., john_doe.jpg).

---
## ✅ How It Works

  - Loads images from the Students/ folder and computes facial encodings.
  - Opens the webcam and reads frames in real-time.
  - Matches detected faces with known encodings.
  - If a match is found and not logged recently, attendance is added to Attendance.csv with a timestamp.

---
## Technologies Used

Python 3, OpenCV, face_recognition, NumPy
