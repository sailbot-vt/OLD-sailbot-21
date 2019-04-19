import numpy as np
import cv2


left = cv2.VideoCapture(0)
right = cv2.VideoCapture(1)
count = 0
while(True):

    # Grab first in order to reduce asynchronous issues and latency
    if not left.grab() or not right.grab():
        print("Frames not grabbed")
        break

    read, left_frame = left.retrieve()
    read, right_frame = right.retrieve()

    cv2.imshow('left', left_frame)
    cv2.imshow('right', right_frame)

    left_img = cv2.cvtColor(left_frame, cv2.COLOR_BGR2GRAY)
    right_img = cv2.cvtColor(right_frame, cv2.COLOR_BGR2GRAY)

    stereo = cv2.StereoBM_create(numDisparities=32, blockSize = 21)
    disparity = stereo.compute(left_img, right_img)

    disparity = disparity.astype(np.uint8)
    cv2.imshow('depth', disparity)

    if cv2.waitKey(33) == 27:
        break
    count += 1
left.release()
right.release()
cv2.destroyAllWindows()