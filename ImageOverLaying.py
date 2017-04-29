import cv2
import numpy as np

mainImage = cv2.imread('images/dog_kitten.jpg')
logoImage = cv2.imread('images/download.png')

#Get size of logo image
rows, cols, channels = logoImage.shape

#get roi matching logo image
roi = mainImage[0:rows, 0:cols]

#convert logo togray scale
logo2Gray = cv2.cvtColor(logoImage, cv2.COLOR_BGR2GRAY)

#apply threashold and get masked image
ret, mask = cv2.threshold(logo2Gray, 240, 255, cv2.THRESH_BINARY_INV)
mask_inv = cv2.bitwise_not(mask)


#take foreground of logo and background of ROI
logo_fg = cv2.bitwise_and(logoImage, logoImage, mask=mask)
logo_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

#add logo_fg & logo_bg
logo_with_bg = cv2.add(logo_fg, logo_bg)

#apply on main image
mainImage[0:rows, 0:cols] = logo_with_bg


cv2.imshow('image with logo', mainImage)

cv2.waitKey(0)
cv2.destroyAllWindows()

