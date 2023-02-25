import cv2
import os
import HandTrackingModule as htm
import numpy as np
###
brushThickness=20
eraserThickness=100
###

folderPath="Header"
l1=os.listdir(folderPath)#Creating & fetching contents from directory
#print(l1)
overlayl1=[]

for i in l1:
    image=cv2.imread(f'{folderPath}/{i}')                                     
    overlayl1.append(image)

#print(len(overlayl1))

header=overlayl1[0]
drawColor=(255,0,255)

    
cap=cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
detector=htm.handDetector(detectionCon=0.90)
xp,yp=0,0
imgCanvas=np.zeros((720,1280,3),np.uint8)

while True:
    success, img=cap.read()#returns boolean and data

    #Find hand landmarks
    img=cv2.flip(img,1)
    img=detector.findHands(img) 
    lmList=detector.findPosition(img,draw=False)

    if len(lmList)!=0:
        
        #print(lmList)

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        #print(fingers)

        #SELECTION MODE - TWo FINGERS ARE Up
        if fingers[1] and fingers[2]:
            xp,yp=0,0 #when hand moved again it will be starts from ,
            
            #print("Selection mode")

            #checking for the click
            if y1<125:
                if 250<x1<450:
                    header =overlayl1[0]
                    drawColor=(255,0,255)
                elif 550 < x1 < 600:
                    header = overlayl1[1]
                    drawColor=(255,0,0)
                
                elif 700 < x1 < 950:
                    header = overlayl1[2]
                    drawColor=(0,255,0)
                
                elif 1050 < x1 < 1200:
                    header = overlayl1[3]
                    drawColor=(0,0,0) #black for eraser
            cv2.rectangle(img, (x1, y1 - 30), (x2, y2 + 30), drawColor, cv2.FILLED)


        #DRAWING MODE
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1 ),25, drawColor, cv2.FILLED)
            #print("Writing mode")
            
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:    
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            xp,yp=x1,y1    
    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)


    img[0:149, 0:1279]=header#regionn of header file
    
    cv2.imshow("Image",img)
    #cv2.imshow("ImgCanvas",imgCanvas)
    #cv2.imshow("Inv",imgInv)
    cv2.waitKey(1)




