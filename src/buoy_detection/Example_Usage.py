from src.buoy_detection.Distance_Calculator import DistanceCalculator

distance_calculator = DistanceCalculator(DRAW_IMAGE= True, camera_numbers=(0,1))

while True:

    left_frame, disparity_frame = distance_calculator.depth_map_calculator.calculateDepthMap()

    buoy_pixel_x, buoy_pixel_y = distance_calculator.findBuoyPixels(left_frame)

    disparity_of_buoy = distance_calculator.getDisparityValue(disparity_frame, buoy_pixel_x, buoy_pixel_y)

    distance_to_buoy = distance_calculator.getDistance(disparity_of_buoy)

    #Get a reading from airmar
    real_bearing_reading_from_airmar = 13
    get_latitude_from_airmar = 21
    get_longitude_from_airmar = 12

    calculated_bearing_to_buoy = distance_calculator.getBearingFromxPixel(buoy_pixel_x, real_bearing_reading_from_airmar)

    estimated_gps_location_of_buoy = \
        distance_calculator.getBuoyGPSLocation(get_latitude_from_airmar, get_longitude_from_airmar, distance_to_buoy, calculated_bearing_to_buoy)

