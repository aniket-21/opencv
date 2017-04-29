import cv2
import numpy as np
#import matplotlib.pyplot as plt

#IMREAD_GRAYSCALE -- 0
#IMREAD_COLOR -- 1
#IMREAD_UNCHANGED -- -1

#Opens an images in grayscale
print(cv2.__version__)
img = cv2.imread("images/dog_kitten.jpg", 1)

part_of_image = img[0:300, 100:400]
img[300:600, 300:600] = part_of_image

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#---------------------------------------------

#Opens and displays a video thru your webcam
# cap = cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('gray', gray)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

# Draw and put test ----------------------------------
# cv2.line(img, (300,0), (500,500), (0, 0, 0), 10) # image , point1, point2, color, thickness
# cv2.rectangle(img, (0,0), (100,100), (255, 255, 255), 15) # image , point1, point2, color, thickness
# cv2.circle(img, (100,63), 55, (0, 255, 8), -1) #image, center, radius, color, fill


###### ROI - region of the imgae
# img[80:100, 70:200] = [67, 90, 17] #Select the region of image and update the pixel color
# part_of_image = img[200:500, 200:500]
# img[600:900, 600:900] = part_of_image


