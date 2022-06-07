import cv2, sys, wx, os.path
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

print('camw is {} camh is {}'.format(camw, camh))
print('Type is {} camh is {}'.format(type(camw), type(camh)))

def getColors():

    f = open('Files/lowerValue.txt','r')
    lines1 =f.readline().split(' ')
    lines1 = np.array([int(i) for i in lines1])
    f.close()

    f = open('Files/upperValue.txt','r')
    lines2 =f.readline().split(' ')
    lines2 = np.array([int(i) for i in lines2])
    f.close()

    return lines1, lines2

def getKernal():

    try:
        k = open('Files/lowerKernal.txt','r')
        kLower = int(k.readline())
        k.close()
    except:
        kLower = 5

    try:
        k = open('Files/upperKernal.txt','r')
        kUpper = int(k.readline())
        k.close()
    except:
        kUpper = 20

    return kLower, kUpper

lbound, ubound = getColors()
lkernal, ukernal = getKernal()

lowerBound = lbound  
upperBound = ubound  

cam= cv2.VideoCapture(0)

cam.set(3,int(camw))
cam.set(4,int(camh))

kernelOpen=np.ones((lkernal,lkernal)) 
kernelClose=np.ones((ukernal,ukernal)) 
pinchFlag=0

while True:
    ret, img=cam.read()
    # img=cv2.resize(img,(camw,camh)) # 340 220

    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    if(len(conts)==2):
        if(pinchFlag==1):
            pinchFlag=0
            mouse.release(Button.left)
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        
        if draw == "0" or 0:
            cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
            cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)

        cx1=int(x1+w1/2)
        cy1=int(y1+h1/2)
        cx2=int(x2+w2/2)
        cy2=int(y2+h2/2)
        cx=int((cx1+cx2)/2)
        cy=int((cy1+cy2)/2)
        
        if draw == "0" or 0:
            cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
            cv2.circle(img, (cx,cy),2,(0,0,255),2)

        mouseLoc=(sx-(cx*sx/camx), cy*sy/camy)
        mouse.position=mouseLoc 


    elif(len(conts)==1):
        x,y,w,h=cv2.boundingRect(conts[0])
        if(pinchFlag==0):
            pinchFlag=1
            mouse.press(Button.left)

        if draw == "0" or 0:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        cx=int(x+w/2)
        cy=int(y+h/2)

        if draw == "0" or 0:
            cv2.circle(img,(cx,cy),int((w+h)/4),(0,0,255),2)

        mouseLoc=(sx-(cx*sx/camx), cy*sy/camy)
        mouse.position=mouseLoc 

    if camera == "0" or 0:
        cv2.imshow("cam",img)
    cv2.waitKey(5)

