# this is heavily based on
# https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
# https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/


# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils #pip install --upgrade imutils
import time

#global variables
north,east,south,west = "Up","Right","Down","Left"

defaultGreenLower = (50,97,0)
defaultGreenUpper = (84,255,255)

defaultRedLower = (0, 179, 106)
defaultRedUpper = (38, 255, 255)

defaultBlueLower = (78, 75, 0)
defaultBlueUpper = (140, 255, 152)


windowTitle = "Tracking & Treshold"
hsvStr = "HSV"

def get_arguments():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    ap.add_argument("-bf", "--buffer", type=int, default=64,
        help="max buffer size")
    ap.add_argument("-t", "--threshold", help="Direction_detection. Lower = more sensitive. Default: 20",default=20,type=int)

    # color flags
    group = ap.add_mutually_exclusive_group()
    group.add_argument("-r", "--red",
        help="track red objects",action='store_true')
    group.add_argument("-b", "--blue",
        help="track blue objects",action='store_true')
    return vars(ap.parse_args())

def callback(value):
    pass


def setup_trackbars(lowerBound, upperBound):
    cv2.namedWindow(windowTitle,0)

    for i in ["MIN", "MAX"]:
        v = lowerBound if i == "MIN" else upperBound

        for j,k in zip(hsvStr,v):
            cv2.createTrackbar("%s_%s" % (j, i), windowTitle, k, 255, callback)

def get_trackbar_values():
    values = []

    for i in ["MIN", "MAX"]:
        for j in hsvStr:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), windowTitle)
            values.append(v)

    return values


def main():
    args = get_arguments()
    
    # initialize the list of tracked points, the frame counter,
    # and the coordinate deltas
    pts = deque(maxlen=args["buffer"])
    counter = 0
    (dX, dY) = (0, 0)
    direction = ""

    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        vs = VideoStream(src=0).start()

    # otherwise, grab a reference to the video file
    else:
        vs = cv2.VideoCapture(args["video"])

    # allow the camera or video file to warm up
    time.sleep(2.0)

    #use green as the default color
    if not args['red'] and not args['blue']:
        setup_trackbars(defaultGreenLower,defaultGreenUpper)
    if args['red']:
        setup_trackbars(defaultRedLower,defaultRedUpper)
    if args['blue']:
        setup_trackbars(defaultBlueLower,defaultBlueUpper)
    if args['threshold']:
        direction_detection = args['threshold']





    # keep looping
    while True:
        # grab the current frame
        frame = vs.read()

        # handle the frame from VideoCapture or VideoStream
        frame = frame[1] if args.get("video", False) else frame
        
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            break
        
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        #flip image
        frame = cv2.flip(frame, 1 )
        #create copy for overlays
        overlay = frame.copy()

        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsvFrame = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        #connect slider to image
        h_min, s_min, v_min, h_max, s_max, v_max = get_trackbar_values()
        
        # construct a mask for the color set at the slider, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        org_mask = cv2.inRange(hsvFrame, (h_min, s_min, v_min), (h_max, s_max, v_max))
        mask = cv2.erode(org_mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(overlay, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(overlay, center, 5, (0, 0, 255), -1)
        
        # update the points queue
        pts.appendleft(center)

        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # check to see if enough points have been accumulated in
            # the buffer
            if counter >= 10 and i == 1 and pts[-10] is not None:
                # compute the difference between the x and y
                # coordinates and re-initialize the direction
                # text variables
                dX = pts[-10][0] - pts[i][0]
                dY = pts[-10][1] - pts[i][1]
                (dirX, dirY) = ("", "")
                # ensure there is significant movement in the
                # x-direction
                if np.abs(dX) > direction_detection:
                    dirX = west if np.sign(dX) == 1 else east
                # ensure there is significant movement in the
                # y-direction
                if np.abs(dY) > direction_detection:
                    dirY = north if np.sign(dY) == 1 else south
                # handle when both directions are non-empty
                if dirX != "" and dirY != "":
                    direction = "{}-{}".format(dirY, dirX)
                # otherwise, only one direction is non-empty
                else:
                    direction = dirX if dirX != "" else dirY
            
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(overlay, pts[i - 1], pts[i], (0, 0, 255), thickness)
        

        # show the movement deltas and the direction of movement on the frame
        cv2.putText(overlay, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,0.65, (0, 0, 255), 2)
        cv2.putText(overlay, "dx: {}, dy: {}".format(dX, dY), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        if direction:
            print(direction)
        
        
        #add third channel to threshold view (required for side-by-side view)
        display_mask1 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

     
        # combine frames into a single window
        gui = np.hstack((overlay, display_mask1))
        
        # display frame
        cv2.imshow(windowTitle,gui)

        key = cv2.waitKey(1) & 0xFF
        counter += 1

        
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            print(get_trackbar_values())
            break

    # if we are not using a video file, stop the camera video stream
    if not args.get("video", False):
        vs.stop()

    # otherwise, release the camera
    else:
        vs.release()

    # close all windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()