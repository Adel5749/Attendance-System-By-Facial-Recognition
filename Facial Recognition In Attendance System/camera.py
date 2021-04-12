import pickle
from model import classNames
import cv2
import numpy as np
import face_recognition
from attendanceMark import WriteAttendees


model=pickle.load(open('model.pkl','rb'))

#print('Encoding Complete')
# End Recognition Code

class VideoCamera(object):


    def __init__(self):
        self.video=cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,frame=self.video.read()

        # Face Recognition code
        imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(model, encodeFace)
            faceDis = face_recognition.face_distance(model, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)
            res=''
            if faceDis[matchIndex] < 0.50:
                name = classNames[matchIndex].upper()
                res=WriteAttendees(name)

            else:
                name = 'Unknown'
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # End Face Recognition Code


        ret,jpeg=cv2.imencode('.jpg',frame)
        return jpeg.tobytes()

