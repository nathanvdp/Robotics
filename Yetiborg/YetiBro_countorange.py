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
maxPower = 1.0

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
 
video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 160) #Width
video_capture.set(4, 120) #Height

orange_lines = 0

def initAngle():
    # Start angle
    PerformMove(0.2, 1.0, 0.25)

def findContours():
    # Capture the frames
        ret, frame = video_capture.read()

        # Crop the image (but actually we dont)
        crop_img = frame[60:120, 0:160]

        # Convert to HSV
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

        lower_orange = np.array([0,50, 50])
        upper_orange = np.array([20, 255, 255])

        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

        # Find the contours of the frame
        return cv2.findContours(mask_orange.copy(), 1, cv2.CHAIN_APPROX_NONE)


max_cx = 1000
      
try:

    ret, frame = video_capture.read()
    raw_input("Press Enter to start")

    initAngle()
    while(True):
        
        contours,hierarchy = findContours()

        # Find the biggest contour (if detected)
        if len(contours) > 0:

            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) >= 500 and orange_lines < 1:
                orange_lines = 1
                PerformMove(1.0, 1.0, 0.05)
            elif cv2.contourArea(c) >= 500 and orange_lines == 1:
                print("Found first line! on to the next..")
                PerformMove(1.0, 1.0, 0.05)
            elif cv2.contourArea(c) >= 500 and orange_lines > 1:
                M = cv2.moments(c)
    
                #cx = 0.0
                #cy = 0.0
                #if M['m00'] != 0:
                #    cx = int(M['m10']/M['m00'])
                #    cy = int(M['m01']/M['m00'])
    
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
    
                #cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
                #cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

                #cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
    
                if cx >= 100 and orange_lines != 2:
                    print("Turn Left!")
                    PerformMove(0.5, 1.0, 0.01)
                elif cx >= 100:
                    print("Found second line!")
                    if cx<max_cx:
                        max_cx = cx
                        # Recovery angle
                        PerformMove(1.0, 0.4, 0.01)
                    else:
                        print("Start tracking normaly..")
                        orange_lines = 3
                        PerformMove(0.5, 1.0, 0.01)

                if cx < 100 and cx > 60:
                    orange_lines = 3
                    print("On Track!")
                    PerformMove(1.0, 1.0, 0.01)

                if cx <= 60:
                    print("Turn Right")
                    PerformMove(1.0, 0.3, 0.01)

            else:
                print("Thought I saw something..")
                PerformMove(1.0, 1.0, 0.01)

        elif orange_lines == 1:
            orange_lines = 2
        else:
            print("Still blind..")
            PerformMove(1.0, 1.0, 0.01)

        #Display the resulting frame
#        cv2.imshow('frame',crop_img)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
except KeyboardInterrupt:
    ZB.MotorsOff()
    