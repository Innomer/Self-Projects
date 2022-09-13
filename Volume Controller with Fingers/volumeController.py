from pickle import NONE, TRUE
from handDetector import handDetector
import cv2 as cv
import math
import numpy as np

from ctypes import  cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

hand_detector=handDetector(min_detection_confidence=0.7)

webCamFeed=cv.VideoCapture(0)

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))

while True:
    isTrue,frame=webCamFeed.read()
    handLandMarks=hand_detector.findHandLandmarks(image=frame,draw=True)

    if len(handLandMarks)!=0:
        x1,y1=handLandMarks[4][1],handLandMarks[4][2] #REfer diagram on mediapipe website for numbering of finger nodes 1 is for x and 2 is for y
        x2,y2=handLandMarks[8][1],handLandMarks[8][2] #we taking thumb and index tip into consideration

        length=math.hypot(x2-x1,y2-y1)
        print(length) #length is 50 when fingers are touched and 250 when wide apart approx
        #Audio level -65.25 means 0 volume and 0 means 100 volume.. therefore we are pairing 50 to -65.25 and 250 to 0

        volumeValue=np.interp(length,[50,250],[-65.25,0])
        volume.SetMasterVolumeLevel(volumeValue,None)

        cv.circle(frame,(x1,y1),15,(255,0,255),cv.FILLED)
        cv.circle(frame,(x2,y2),15,(255,0,255),cv.FILLED)
        cv.line(frame,(x1,y1),(x2,y2),(255,0,255),3)

    cv.imshow('VC',frame)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
webCamFeed.release()
cv.destroyAllWindows()
cv.waitKey(0)