from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np 
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch(("SAPI.Spvoice"))
    speak.Speak(str1)

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

if not os.path.exists('data/'):  # check that the data folder exists or not, if not then it creates itself 
    os.makedirs('data/')

with open('data/names.pkl', 'rb') as f:
    LABELS = pickle.load(f)

with open('data/faces_data.pkl', 'rb') as f:
    faces = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors=5)

knn.fit(faces, LABELS)
imgBackground = cv2.imread("voting.jpg")

COL_NAMES = ['NAME', 'VOTE', 'DATE', 'TIME']
output=[None]

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert each frame to the gray scale
    faces = facedetect.detectMultiScale(gray, 1.3, 5)  # detect the face from each frame 
    for (x, y, w, h) in faces: 
        crop_img = frame[y:y+h , x:x+w]  # crop the face from the picture 
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img) 
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")   
        exist = os.path.isfile("Votes.csv")
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        attendance = [output[0], timestamp]
    
    # Resize webcam frame to fit the white box space
    resized_frame = cv2.resize(frame, (360, 435))  # Adjusted to match the image proportions
    # Paste the resized frame onto the background image at the left section
    imgBackground[90:525, 70:430] = resized_frame  # Make sure this fits your imgBackground size

    cv2.imshow('frame', imgBackground)
    k = cv2.waitKey(1)

    def check_if_exists(value):
        try:
            with open("Votes.csv","r") as csvfile:
                reader=csv.reader(csvfile)
                for row in reader:
                    if row and row[0]==value:
                     return True         
        except FileNotFoundError:
            print("File not found or unable to open the CSV file.")
        return False
    
    voter_exist =check_if_exists(output[0])
    if voter_exist:
        print("you have already voted")
        speak("you have already voted")
        break
    if k==ord('1'):
         speak("your vote has been recorded")
         time.sleep(3)
         if exist:
             with open ("Votes" + ".csv","+a") as csvfile:
                 writer=csv.writer(csvfile)
                 attendance=[output[0],"BJP",date,timestamp]
                 writer.writerow(attendance)
             csvfile.close()
         else:
             if exist:
                with open ("Votes" + ".csv","+a") as csvfile:
                 writer=csv.writer(csvfile)
                 attendance=[output[0],"BJP",date,timestamp]
                 writer.writerow(attendance)
                csvfile.close()
         speak("thank you for participation in the elections")
         break

    if k==ord('2'):
         speak("your vote has been recorded")
         time.sleep(3)
         if exist:
             with open ("Votes" + ".csv","+a") as csvfile:
                 writer=csv.writer(csvfile)
                 attendance=[output[0],"CONGRESS",date,timestamp]
                 writer.writerow(attendance)
             csvfile.close()
         else:
             if exist:
                with open ("Votes" + ".csv","+a") as csvfile:
                 writer=csv.writer(csvfile)
                 attendance=[output[0],"CONGRESS",date,timestamp]
                 writer.writerow(attendance)
                csvfile.close()
         speak("thank you for participation in the elections")
         break
    
    if k==ord('3'):
         speak("your vote has been recorded")
         time.sleep(3)
         if exist:
             with open ("Votes" + ".csv","+a") as csvfile:
                 writer=csv.writer(csvfile)
                 attendance=[output[0],"AAP",date,timestamp]
                 writer.writerow(attendance)
             csvfile.close()
         else:
             if exist:
                with open ("Votes" + ".csv","+a") as csvfile:
                 writer=csv.writer(csvfile)
                 attendance=[output[0],"AAP",date,timestamp]
                 writer.writerow(attendance)
                csvfile.close()
         speak("thank you for participation in the elections")
         break
    
    if k==ord('4'):
         speak("your vote has been recorded")
         time.sleep(3)
         if exist:
             with open ("Votes" + ".csv","+a") as csvfile:
                 writer=csv.writer(csvfile)
                 attendance=[output[0],"NOTA",date,timestamp]
                 writer.writerow(attendance)
             csvfile.close()
         else:
             if exist:
                with open ("Votes" + ".csv","+a") as csvfile:
                 writer=csv.writer(csvfile)
                 attendance=[output[0],"NOTA",date,timestamp]
                 writer.writerow(attendance)
                csvfile.close()
         speak("thank you for participation in the elections")
         break

video.release()
cv2.destroyAllWindows()  

