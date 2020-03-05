#!/usr/bin/python
import numpy as np
import cv2
import ZeroBorg
import time
import math
import sys

video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 160)
video_capture.set(4, 120)

# Capture the frames
ret, frame = video_capture.read()

cv2.imwrite('frame.jpg', frame)

# Crop the image
crop_img = frame[60:120, 0:160]
cv2.imwrite('crop.jpg', crop_img)

# Convert to grayscale
gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray.jpg', gray)

edges = cv2.Canny(gray,50,200)
cv2.imwrite('edges.jpg', edges)
	
lines = cv2.HoughLines(edges,1,np.pi/180,50)
draw_line = np.zeros((60,160))
if lines is not None:

	for line in lines:
		
		rho,theta = line[0]
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))
		#x1, y1, x2, y2 = line[0]
		cv2.line(draw_line, (x1,y1),(x2,y2), (255,0,0),3)
cv2.imwrite('lines.jpg',draw_line)

lower = np.uint8([100,0,0])
upper = np.uint8([160,100,100])

white_mask = cv2.inRange(crop_img,lower,upper)
cv2.imwrite('mask.jpg',white_mask)

blue = crop_img[:,:,0]
cv2.imwrite('blue.jpg', blue)

red = crop_img[:,:,2]
cv2.imwrite('red.jpg', red)

# Gaussian blur
blur = cv2.GaussianBlur(blue,(5,5),0)
cv2.imwrite('blur.jpg', blur)

# Color thresholding
ret_b,thresh_b = cv2.threshold(blue,100,255,cv2.THRESH_BINARY)
cv2.imwrite('thresh_b.jpg', thresh_b)

ret_r, thresh_r = cv2.threshold(red, 130, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite('thresh_r.jpg', thresh_r)

thresh = np.fmod(thresh_b+thresh_r,255)
print(thresh)

# Find the contours of the frame
contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
