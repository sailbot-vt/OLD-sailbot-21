import cv2

LEFT_PATH = "/home/wlans4/PycharmProjects/sailbot-19/src/buoy_detection/buoy_detection/LEFT/{:01d}.png"
RIGHT_PATH = "/home/wlans4/PycharmProjects/sailbot-19/src/buoy_detection/buoy_detection/RIGHT{:01d}.png"

left = cv2.VideoCapture(0)
right = cv2.VideoCapture(1)

frame_count = 0

while True:

    if not left.grab() or not right.grab():
        print("Frames not grabbed")
        break
    grabbed, left_frame = left.retrieve()
    grabbed, right_frame = right.retrieve()
    cv2.imshow('left', left_frame)
    cv2.imshow('right', right_frame)
    key = cv2.waitKey(1)
    if key%256 == 32:
        cv2.imwrite(LEFT_PATH.format(frame_count), left_frame)
        cv2.imwrite(RIGHT_PATH.format(frame_count), right_frame)
        frame_count += 1
    elif key%256 == 27:
        break
    if frame_count >= 25:
        break

left.release()
right.release()
cv2.destroyAllWindows()