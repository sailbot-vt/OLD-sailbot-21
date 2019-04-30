import cv2
import glob
import os

CHESSBOARD_CALIBRATION_SIZE = (5,7)
IMAGES_TO_TAKE = 200
left = cv2.VideoCapture(0)
right = cv2.VideoCapture(1)
DRAW_IMAGE = True

# Create the paths to store images if they do not exist yet
path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
LEFT_PATH = path + "LEFT"
RIGHT_PATH = path + "RIGHT"

if not os.path.exists(LEFT_PATH):
    try:
        os.mkdir(LEFT_PATH)
    except:
        pass
if not os.path.exists(RIGHT_PATH):
    try:
        os.mkdir(RIGHT_PATH)
    except:
        pass



LEFT = LEFT_PATH + "{:01d}.png"
RIGHT = RIGHT_PATH + "{:01d}.png"
frame_count = 0

#Clear out the directory first
for f in glob.glob(LEFT_PATH + "/*"):
    os.remove(f)
for f in glob.glob(RIGHT_PATH + "/*"):
    os.remove(f)


while True:

    if not left.grab() or not right.grab():
        print("Frames not grabbed")
        break
    grabbed, left_frame = left.retrieve()
    grabbed, right_frame = right.retrieve()

    if DRAW_IMAGE:
        cv2.imshow('left', left_frame)
        cv2.imshow('right', right_frame)
    key = cv2.waitKey(1)
    if key%256 == 32:
        cv2.imwrite(LEFT.format(frame_count), left_frame)
        cv2.imwrite(RIGHT.format(frame_count), right_frame)
        frame_count += 1
    elif key%256 == 27:
        break
    if frame_count >= IMAGES_TO_TAKE:
        break

left.release()
right.release()


