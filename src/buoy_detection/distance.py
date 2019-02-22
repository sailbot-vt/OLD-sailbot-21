#Distance between the two cameras in cm
camera_distance = 1
#Focal length of the camera lenses in mm
focal_length = 1
#Camera angle in degrees
theta = 20
#Disparity of an object based on the difference of left and right images
image_disparity = []


import cv2

left = cv2.VideoCapture(0)
right = cv2.VideoCapture(1)

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

left.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
right.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

while(True):
    if not (left.grab() and right.grab()):
        print("No more frames")
        break

    _, leftFrame = left.retrieve()
    _, rightFrame = right.retrieve()

    cv2.imshow('left', leftFrame)
    cv2.imshow('right', rightFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

left.release()
right.release()
cv2.destroyAllWindows()
cv2.destroyAllWindows()