import time
import cv2
import numpy as np

detector = cv2.CascadeClassifier('eyedetect.xml')
cap = cv2.VideoCapture(1)
while True:

    cv_image, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    if len(faces) >= 1:
        print("发现{0}个人脸!".format(len(faces)))

    for (x, y, w, h) in faces:
        # cv2.rectangle(image,(x,y),(x+w,y+w),(0,255,0),2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow('frame', frame)
    # pygame.image.save(image, "pygame1.jpg")
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()