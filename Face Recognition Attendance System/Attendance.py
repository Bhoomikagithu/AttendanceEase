import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
import pandas as pd

def findEncodings(images):
    encodeList = []
    for img in images:
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                encodeList.append(encodings[0])
    return encodeList

def markAttendance(name):
    filename = 'Attendance.csv'
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')
    # Create file with header if not exists
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
        df.to_csv(filename, index=False)
    df = pd.read_csv(filename)
    # Prevent duplicate entry for the same person same day
    if not ((df['Name'] == name) & (df['Date'] == date_str)).any():
        new_row = pd.DataFrame([[name, date_str, time_str]], columns=["Name", "Date", "Time"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(filename, index=False)

def run_webcam_recognition():
    path = 'Students'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        if curImg is None:
            print(f"Image {cl} not loaded correctly.")
            continue
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        print(classNames)
    encodeKnown = findEncodings(images)
    print('Encoding Complete')
    cap = cv2.VideoCapture(0)
    recognition_times = {}
    try:
        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesInFrame = face_recognition.face_locations(imgS)
            encodesInFrame = face_recognition.face_encodings(imgS, facesInFrame)
            for encodeFace, faceLoc in zip(encodesInFrame, facesInFrame):
                matches = face_recognition.compare_faces(encodeKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex] and faceDis[matchIndex] < 0.5:
                    name = classNames[matchIndex].upper()
                else:
                    name = 'UNKNOWN'
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0))
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                if name != 'UNKNOWN':
                    now = datetime.now()
                    if name in recognition_times:
                        if now - recognition_times[name] >= timedelta(seconds=3):
                            markAttendance(name)
                            del recognition_times[name]
                    else:
                        recognition_times[name] = now
            current_time = datetime.now()
            recognition_times = {name: time for name, time in recognition_times.items() if current_time - time < timedelta(seconds=3)}
            cv2.imshow('Webcam', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
