import numpy as np
import cv2



def nothing(x):
    pass

#Create the trackbar to detect HSV Values
cv2.namedWindow('HSV', cv2.WINDOW_AUTOSIZE)

# create trackbars for color change
cv2.createTrackbar('Hmin','HSV',10,255,nothing)
cv2.createTrackbar('Smin','HSV',10,255,nothing)
cv2.createTrackbar('Vmin','HSV',10,255,nothing)
cv2.createTrackbar('Hmax','HSV',50,255,nothing)
cv2.createTrackbar('Smax','HSV',50,255,nothing)
cv2.createTrackbar('Vmax','HSV',50,255,nothing)



cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cv2.resize(frame, (100,50)) #resize
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #BGR -> HSV

    Hmax = cv2.getTrackbarPos('Hmax', 'HSV')
    Smax = cv2.getTrackbarPos('Smax', 'HSV')
    Vmax = cv2.getTrackbarPos('Vmax', 'HSV')

    Hmin = cv2.getTrackbarPos('Hmin', 'HSV')
    Smin = cv2.getTrackbarPos('Smin', 'HSV')
    Vmin = cv2.getTrackbarPos('Vmin', 'HSV')

    lower_red = np.array([Hmin, Smin, Vmin])
    upper_red = np.array([Hmax, Smax, Vmax])

    mask = cv2.inRange(imgHSV, lower_red, upper_red)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    #cv2.imshow('closing', frame)
    cv2.imshow('Result', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()