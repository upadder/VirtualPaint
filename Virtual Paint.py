import cv2
import numpy as np
framewidth=700
frameheight=480
cap=cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,160)

myColors=[[0,195,101,70,255,255],[51,130,90,179,233,204],[20,106,111,72,255,255],[130,151,68,179,173,190]]

myColorValues=[[55,175,212],[102,102,255],[0,255,213],[0,0,255]]    #BGR

myPoints=[]



def findColor(img,myColors,myColorValues):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for i in myColors:
        lower = np.array(i[0:3])
        upper = np.array(i[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
    return newPoints


def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for i in contours:
        area=cv2.contourArea(i)
        if area>500:
            # cv2.drawContours(imgResult, i, -1, (255, 0, 0), 3)
            peri=cv2.arcLength(i,True)
            approx=cv2.approxPolyDP(i,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y
def drawOnCanvas(myPoints,myColorValue):
    for i in myPoints:
        cv2.circle(imgResult, (i[0], i[1]), 10, myColorValues[i[2]], cv2.FILLED)

while True:
    success,img=cap.read()
    imgResult=img.copy()
    newPoints=findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newp in newPoints:
            myPoints.append(newp)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Output",imgResult)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break