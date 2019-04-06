import cv2
import numpy as np
left = cv2.VideoCapture(0)
right = cv2.VideoCapture(1)

CHESSBOARD_CALIBRATION_SIZE = (6, 9)


left.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
left.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
right.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
right.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
while(True):

    # Grab first in order to reduce asynchronous issues and latency
    if not left.grab() or not right.grab():
        print("Frames not grabbed")
        break

    read, left_frame = left.retrieve()
    read, right_frame = right.retrieve()

    cv2.imshow('left', left_frame)
    cv2.imshow('right', right_frame)

    if cv2.waitKey(33) == 27:
        break

left.release()
right.release()
cv2.destroyAllWindows()