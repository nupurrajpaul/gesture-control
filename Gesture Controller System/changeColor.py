import cv2 
import numpy as np

fl = 0

def nothing(x):
    pass

lowerBound=np.array([0,1,0]) #[0,132,0]
upperBound=np.array([32,14,12]) #[141,255,87]

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

cap = cv2.VideoCapture(0)

# getting color values and kernal values
f = open('Files/lowerValue.txt','r')
lines1 =list(f.readline().split(' '))
# lines1 = np.array([int(i) for i in lines1])
f.close()

f = open('Files/upperValue.txt','r')
lines2 =list(f.readline().split(' '))
# lines2 = np.array([int(i) for i in lines2])
f.close()

f = open('Files/upperKernal.txt','r')
k1 = int(f.readline())
f.close()

f = open('Files/lowerKernal.txt','r')
k2 = int(f.readline())
f.close()

cv2.namedWindow('frame')
cv2.namedWindow('tbar')
cv2.resizeWindow('tbar', 400, 350)

cv2.createTrackbar('lowerBlue','tbar',int(lines1[0]),255,nothing) # lines1[0]
cv2.createTrackbar('lowerGreen','tbar',int(lines1[1]),255,nothing) # lines1[1]
cv2.createTrackbar('lowerRed','tbar',int(lines1[2]),255,nothing) # lines1[2]

cv2.createTrackbar('upperBlue','tbar',int(lines2[0]),255,nothing) # lines2[0]
cv2.createTrackbar('upperGreen','tbar',int(lines2[1]),255,nothing) # lines2[1]
cv2.createTrackbar('upperRed','tbar',int(lines2[2]),255,nothing) # lines2[2]

cv2.createTrackbar('KernalOpen','tbar',k1,50,nothing) # k1
cv2.createTrackbar('KernalClose','tbar',k2,50,nothing) # k2

font = cv2.FONT_HERSHEY_COMPLEX

def setColor():
    lb = lowerblue
    lg = lowergreen
    lr = lowerred

    ub = upperblue
    ug = uppergreen
    ur = upperred

    f = open('Files/lowerValue.txt','w')
    f.write('{} {} {}'.format(lb,lg,lr))
    f.close()

    f = open('Files/upperValue.txt','w')
    f.write('{} {} {}'.format(ub,ug,ur))
    f.close()

    exit()

def setKernal():
    kopen = kernelOpen
    kclose = kernelClose

    k = open('FIles/lowerKernal.txt','w')
    k.write(str(len(kopen)))
    k.close()

    k = open('FIles/upperKernal.txt','w')
    k.write(str(len(kclose)))
    k.close()

def mouse_click(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        LB = 'left'
        color = img[x,y]
        print(color)


cv2.setMouseCallback('frame',mouse_click)
while True:
    _, img = cap.read()

    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose

    imgbit = cv2.bitwise_and(img,img,mask = maskFinal)

    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    if len(conts)==1:
        x,y,w,h=cv2.boundingRect(conts[0])
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    upperblue = cv2.getTrackbarPos('upperBlue','tbar')
    uppergreen = cv2.getTrackbarPos('upperGreen','tbar')
    upperred = cv2.getTrackbarPos('upperRed','tbar')

    lowerblue = cv2.getTrackbarPos('lowerBlue','tbar')
    lowergreen = cv2.getTrackbarPos('lowerGreen','tbar')
    lowerred = cv2.getTrackbarPos('lowerRed','tbar') 

    KernalOpen = cv2.getTrackbarPos('KernalOpen','tbar')
    KernalClose = cv2.getTrackbarPos('KernalClose','tbar')

    lowerBound[0] = lowerblue
    lowerBound[1] = lowergreen
    lowerBound[2] = lowerred

    upperBound[0] = upperblue
    upperBound[1] = uppergreen
    upperBound[2] = upperred

    kernelOpen = np.ones((KernalOpen,KernalOpen))  
    kernelClose = np.ones((KernalClose,KernalClose)) 

    cv2.putText(img,str(lowerblue),(10,150),font,1,(0,0,255))
    cv2.putText(img,str(lowergreen),(10,180),font,1,(0,0,255))
    cv2.putText(img,str(lowerred),(10,210),font,1,(0,0,255))

    cv2.putText(img,str(upperblue),(10,30),font,1,(0,0,255))
    cv2.putText(img,str(uppergreen),(10,60),font,1,(0,0,255))
    cv2.putText(img,str(upperred),(10,90),font,1,(0,0,255))

    cv2.putText(img,'Press Enter to Apply !...',(10,120),font,1,(0,0,255))

    cv2.imshow('frame',img)
    cv2.imshow('grey',maskFinal) 
    cv2.imshow('bitwise',imgbit)  #imgHSV
    key = cv2.waitKey(1)

    if key == 27:
        break
    if key == 13:
        setColor()
        setKernal()

cap.release()