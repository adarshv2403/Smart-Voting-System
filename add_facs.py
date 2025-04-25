import cv2
import pickle
import numpy as np
import os

# Create 'data/' directory if it doesn't exist
if not os.path.exists('data/'):
    os.makedirs('data/')

# Start webcam
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

faces_data = []  # To store face images
i = 0
name = input("Enter your Aadhar number: ").strip()  # Collect user input

framesTotal = 51              # Total number of face images to collect
captureAfterFrames = 2        # Capture every 2nd frame

while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50))

        if len(faces_data) < framesTotal and i % captureAfterFrames == 0:
            faces_data.append(resized_img)
        i += 1

        cv2.putText(frame, f'Captured: {len(faces_data)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) >= framesTotal:
        break

video.release()
cv2.destroyAllWindows()

# Convert list to numpy array and reshape
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape((faces_data.shape[0], -1))  # (51, 7500)
print(f"Total face samples collected: {len(faces_data)}")

# Save names
names_file = 'data/names.pkl'
if not os.path.exists(names_file):
    names = [name] * framesTotal
    with open(names_file, 'wb') as f:
        pickle.dump(names, f)
else:
    with open(names_file, 'rb') as f:
        names = pickle.load(f)
    names += [name] * framesTotal
    with open(names_file, 'wb') as f:
        pickle.dump(names, f)

# Save face data
faces_file = 'data/faces_data.pkl'
if not os.path.exists(faces_file):
    with open(faces_file, 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open(faces_file, 'rb') as f:
        existing_faces = pickle.load(f)
    updated_faces = np.append(existing_faces, faces_data, axis=0)
    with open(faces_file, 'wb') as f:
        pickle.dump(updated_faces, f)
