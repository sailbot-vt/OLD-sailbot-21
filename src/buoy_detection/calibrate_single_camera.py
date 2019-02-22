import cv2

class calibrate_single_camera:
    def __init__(self, camera_number = 0, camera_width = 1280, camera_height = 720):
        CAM_NUMBER = camera_number
        CAMERA_WIDTH = camera_width
        CAMERA_HEIGHT = camera_height

        # Calibrating the left camera
        if CAM_NUMBER == 0:
            image_path = "./camera_capture/left/{.06d}.jpg"
        # Calibrating the right camera
        elif CAM_NUMBER == 1:
            image_path = "./camera_capture/right/{.06d}.jpg"
        else:
            raise Exception("Please input a valid camera number")

        cam = cv2.VideoCapture(CAM_NUMBER)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

        frame_id = 0
        while (frame_id < 50):
            frame = cam.read()
            cv2.imwrite(image_path.format(frame_id), frame)
            frame_id += 1
        frameId = 0


