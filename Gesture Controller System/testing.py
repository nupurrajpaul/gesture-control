from tkinter import messagebox
import sys 

try:
    n=len(sys.argv[1])
    a=sys.argv[1][0:n]
    a=a.split(',')
    camw = a[0].replace("'",'')
    camh = a[1].replace("'",'')
except:
    camw = 640
    camh = 480

try:
	import cv2, math, time, sys, wx
	import mediapipe as mp
	import mediaPipeCus as htm
	import numpy as np
	from pynput.mouse import Button, Controller
except:
	messagebox.showinfo("Warning", "Some Modules are missing ! Try pip install...")
	exit()


try:
	cap = cv2.VideoCapture(0)
	cap.set(3,int(camw))
	cap.set(4,int(camh))
except:
	messagebox.showinfo("Warning", "Camera not found...")
	exit()

font = cv2.FONT_HERSHEY_COMPLEX
detector = htm.handDetector(detectionCon=0.8)

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    img, num = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False, handNo=0)

    if lmList:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1),5,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),5,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),8,(255,0,255),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)

        if length <30:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
 
    img = cv2.flip(img, 1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img,"Mouse is working",(10,50),font,1,(0,0,255))
    cv2.putText(img,"Camera is working...",(10,100),font,1,(0,0,255))
    cv2.putText(img,"Fps : {}".format(str(fps)),(10,150),font,1,(0,0,255))

    cv2.imshow("Image", img)
    cv2.waitKey(1)