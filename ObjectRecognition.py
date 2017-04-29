import numpy as np
import cv2



# def nothing(x):
#     pass
#
# #Create the trackbar to detect HSV Values
# cv2.namedWindow('HSV', cv2.WINDOW_AUTOSIZE)
#
# # create trackbars for color change
# cv2.createTrackbar('Hmin','HSV',10,255,nothing)
# cv2.createTrackbar('Smin','HSV',10,255,nothing)
# cv2.createTrackbar('Vmin','HSV',10,255,nothing)
# cv2.createTrackbar('Hmax','HSV',50,255,nothing)
# cv2.createTrackbar('Smax','HSV',50,255,nothing)
# cv2.createTrackbar('Vmax','HSV',50,255,nothing)



cap = cv2.VideoCapture(0)


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cv2.resize(frame, (100,50)) #resize
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #BGR -> HSV

    # Hmax = cv2.getTrackbarPos('Hmax', 'HSV')
    # Smax = cv2.getTrackbarPos('Smax', 'HSV')
    # Vmax = cv2.getTrackbarPos('Vmax', 'HSV')
    #
    # Hmin = cv2.getTrackbarPos('Hmin', 'HSV')
    # Smin = cv2.getTrackbarPos('Smin', 'HSV')
    # Vmin = cv2.getTrackbarPos('Vmin', 'HSV')

    lower_red = np.array([0, 166, 120])
    upper_red = np.array([25, 255, 255])

    # # Normal masking algorithm
    # lower_red = np.array([108, 61, 90])
    # upper_red = np.array([255, 255, 255])

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
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

        #cv2.drawContours(frame, contours, i, (0, 255, 0), 3)

    # # Display the resulting frame
    # cv2.imshow('erode', erosion)
    cv2.imshow('closing', frame)
    #cv2.imshow('Result', mask)

    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()