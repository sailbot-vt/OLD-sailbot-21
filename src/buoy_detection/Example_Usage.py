from src.buoy_detection.Distance_Calculator import DistanceCalculator


"""
This  file gives an example of how the CV functions can be used


There is a function named getCameraNumbers() in test_cameras.py that will tell you which cameras to use when creating your distance calculator.
These numbers change for different computers, so I am not sure if they will stay as (2,3) when instantiating a distance calculator
"""

distance_calculator = DistanceCalculator(DRAW_IMAGE= True, camera_numbers=(2,3))

while True:

    #Pull frames from the cameras and fix their distortions using the calibration. Then create a depth map
    try:
        left_frame, disparity_frame = distance_calculator.depth_map_calculator.calculateDepthMap()
    except:
        continue
    #Determine where in the image is the buoy, if any. If there is a buoy, return the pixels at which it is found
    try:
        buoy_pixel_x, buoy_pixel_y = distance_calculator.findBuoyPixels(left_frame)
    except:
        continue
    #Get the disparity value of the pixels found
    disparity_of_buoy = distance_calculator.getDisparityValue(disparity_frame, buoy_pixel_x, buoy_pixel_y)

    #Calculate the distance to the buoy using the disparity values
    distance_to_buoy = distance_calculator.getDistance(disparity_of_buoy)

    #Get a reading from airmar
    real_bearing_reading_from_airmar = 13
    get_latitude_from_airmar = 21
    get_longitude_from_airmar = 12

    #Calculate the angle to the buoy in the x directions
    calculated_bearing_to_buoy = distance_calculator.getBearingFromxPixel(buoy_pixel_x, real_bearing_reading_from_airmar)

    #Estimate the GPS location of the buoy using the angle in the x direction, current GPS coordinates, and distance to the buoy
    estimated_gps_location_of_buoy = \
        distance_calculator.getBuoyGPSLocation(get_latitude_from_airmar, get_longitude_from_airmar, distance_to_buoy, calculated_bearing_to_buoy)

