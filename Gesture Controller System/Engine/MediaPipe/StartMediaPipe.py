import cv2, math, time, sys, wx
import mediapipe as mp
import mediaPipeCus as htm
import numpy as np
from pynput.mouse import Button, Controller

try:
    n=len(sys.argv[1])
    a=sys.argv[1][0:n]
    a=a.split(',')
    camera = a[0].replace("'",'')
    draw = a[1]
    camw = a[2]
    camh = a[3].replace("'",'')
except:
    camera = 0
    draw = 0
    camw = 320
    camh = 240

mouse=Controller()

app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(int(camw),int(camh))

cap = cv2.VideoCapture(0)
cap.set(3,int(camw))
cap.set(4,int(camh))

pTime = 0
cTime = 0

detector = htm.handDetector(detectionCon=0.9)

while True:
    success, img = cap.read()

    if draw == "0" or 0:
        img, num = detector.findHands(img, draw=True)
    if draw == "1" or 1:
        img, num = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False, handNo=0)

    if lmList:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        if draw == "0" or 0:
            cv2.circle(img,(x1,y1),5,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),5,(255,0,255),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            cv2.circle(img,(cx,cy),8,(255,0,255),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)

        if length <40:
            if draw == "0" or 0:
                cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
            mouse.press(Button.left)
        else:
            print('...')
            mouse.release(Button.left)

        mouseLoc=(sx-(cx*sx/camx), (cy*sy/camy))
        mouse.position=mouseLoc 
 
    img = cv2.flip(img, 1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    if camera == "0" or 0: 
        cv2.imshow("Image", img)
    cv2.waitKey(1)