import cv2

left = cv2.VideoCapture(0)
right = cv2.VideoCapture(2)
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