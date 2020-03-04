#!/usr/bin/python
#coding:  Latin-1

# Import library functions we need
import numpy as np
import cv2
import ZeroBorg
import time
import math
import sys

# Setup the ZeroBorg
ZB = ZeroBorg.ZeroBorg()
ZB.Init()
if not ZB.foundChip:
    boards = ZeroBorg.ScanForZeroBorg()
    if len(boards) == 0:
        print 'No ZeroBorg found, check you are attached :)'
    else:
        print 'No ZeroBorg at address %02X, but we did find boards:' % (ZB.i2cAddress)
        for board in boards:
            print '    %02X (%d)' % (board, board)
        print 'If you need to change the I²C address change the setup line so it is correct, e.g.'
        print 'ZB.i2cAddress = 0x%02X' % (boards[0])
    sys.exit()
ZB.SetCommsFailsafe(False)             # Disable the communications failsafe
ZB.ResetEpo()

# Power settings
voltageIn = 9.0                         # Total battery voltage to the ZeroBorg (change to 9V if using a non-rechargeable battery)
voltageOut = 9.0                        # Maximum motor voltage

# Setup the power limits
if voltageOut > voltageIn:
    maxPower = 0.5
else:
    maxPower = voltageOut / float(voltageIn)

# Function to perform a general movement
def PerformMove(driveLeft, driveRight, numSeconds):
    # Set the motors running
    ZB.SetMotor1(-driveRight * maxPower) # Rear right
    ZB.SetMotor2(-driveRight * maxPower) # Front right
    ZB.SetMotor3(-driveLeft  * maxPower) # Front left
    ZB.SetMotor4(-driveLeft  * maxPower) # Rear left
    # Wait for the time
    time.sleep(numSeconds)
    # Turn the motors off
    ZB.MotorsOff()
 
video_capture = cv2.VideoCapture(0)
#video_capture.set(3, 160) #Width
#video_capture.set(4, 120) #Height
      
try:
    while(True):
        # Capture the frames
        ret, frame = video_capture.read()

        # Crop the image
        crop_img = frame#[60:120, 0:160]

        # Convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # Gaussian blur
        blur = cv2.GaussianBlur(gray,(5,5),0)

        # Color thresholding
        ret,thresh = cv2.threshold(blur,130,255,cv2.THRESH_BINARY)

        # Find the contours of the frame
        contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # Find the biggest contour (if detected)
        if len(contours) > 0:

            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
'''
            cx = 0.0
            cy = 0.0
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
'''
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
'''
            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
'''
            if cx >= 120:
                print("Turn Left!")
                PerformMove(-1.0, 1.0, 0.02)

            if cx < 120 and cx > 50:
                print("On Track!")
                PerformMove(1.0, 1.0, 0.02)

            if cx <= 50:
                print("Turn Right")
                PerformMove(1.0, -1.0, 0.02)

        else:
            print("I don't see the line")
            PerformMove(-1.0, -0.5, 0.05)
            PerformMove(-1.0, -1.0, 0.05)
            PerformMove(-0.5, -1.0, 0.05)
            PerformMove(-1.0, -1.0, 0.05)

        #Display the resulting frame
#        cv2.imshow('frame',crop_img)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
except KeyboardInterrupt:
    ZB.MotorsOff()
    