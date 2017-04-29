import cv2
import numpy as np

frame = cv2.imread("images/pink.jpg", 1)

#converting to HSV
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

# Normal masking algorithm
lower_green = np.array([140 ,0,0])
upper_green = np.array([165,255,255])


mask = cv2.inRange(hsv,lower_green, upper_green)

#shows only green stuff
result = cv2.bitwise_and(frame,frame,mask = mask)

cv2.imshow('original', frame)
cv2.imshow('result',result)
cv2.waitKey(0)
cv2.destroyAllWindows()