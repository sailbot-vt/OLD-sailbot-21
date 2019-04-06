from math import tan, atan

#We need the full camera capture angle/2

def calculate_angle_left_camera(left_camera_width, left_camera_pixel, distance_to_object):
    width = left_camera_width/2
    a1 = atan((left_camera_pixel - width)/width
