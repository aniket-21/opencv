import numpy as np
import cv2
import time
import wiringpi as wpi
from picamera.array import PiRGBArray
from picamera import PiCamera

#Use Pi Camera
camera = PiCamera()
camera.resolution = (640,480)
camera.vflip = True
camera.hflip = True
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

#Define pins
wpi.wiringPiSetup()
pin1 = 7
pin2 = 11
pin3 = 13
pin4 = 15

#Set Pin Modes
wpi.pinMode(pin1, 1)
wpi.pinMode(pin2, 1)
wpi.pinMode(pin3, 1)
wpi.pinMode(pin4, 1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Capture frame-by-frame
    frame = rawCapture.array
    cv2.resize(frame, (160,120)) #resize
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #BGR -> HSV

    lower_red = np.array([40, 76, 111])
    upper_red = np.array([73, 255, 255])

    mask = cv2.inRange(imgHSV, lower_red, upper_red)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    #some morphological transformations
    kernel = np.ones((5,5),  np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    #finding contours and getting the biggest one
    _, contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if(len(contours) > 0):
        perimeters = [cv2.arcLength(contour, False) for contour in contours]
        i = np.argmax(perimeters)
        rect = cv2.minAreaRect(contours[i])
        center, size, angle = rect
        print("X:{} Y:{}".format(center[0], center[1]))
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
        #cv2.drawContours(frame, contours, i, (0, 255, 0), 3)

	#Check center and move the bot
        if(center[1] < 280):
	    #forward 0-1-0-1
	    wpi.digitalWrite(pin1, 0)
	    wpi.digitalWrite(pin2, 1)
	    wpi.digitalWrite(pin3, 0)
	    wpi.digitalWrite(pin4, 1)
	    wpi.delay(250)
	    wpi.digitalWrite(pin1, 0)
	    wpi.digitalWrite(pin2, 0)
	    wpi.digitalWrite(pin3, 0)
	    wpi.digitalWrite(pin4, 0)

        if(center[0] < 310):
	    #right 1-1-0-1
	    wpi.digitalWrite(pin1, 1)
	    wpi.digitalWrite(pin2, 1)
	    wpi.digitalWrite(pin3, 0)
	    wpi.digitalWrite(pin4, 1)    
	    wpi.delay(100)    
	    wpi.digitalWrite(pin1, 0)
	    wpi.digitalWrite(pin2, 0)
	    wpi.digitalWrite(pin3, 0)
	    wpi.digitalWrite(pin4, 0)
	    
        if(center[0] > 340):
	    #right 1-1-0-1
	    wpi.digitalWrite(pin1, 0)
	    wpi.digitalWrite(pin2, 1)
	    wpi.digitalWrite(pin3, 1)
	    wpi.digitalWrite(pin4, 1) 
	    wpi.delay(100) 
	    wpi.digitalWrite(pin1, 0)
	    wpi.digitalWrite(pin2, 0)
	    wpi.digitalWrite(pin3, 0)
	    wpi.digitalWrite(pin4, 0)

    # Display the resulting frame
    # cv2.imshow('erode', erosion)
    cv2.imshow('closing', frame)
    #cv2.imshow('Result', mask)

    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()