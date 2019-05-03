from src.buoy_detection.Distance_Calculator import DistanceCalculator

while True:

    #
    distance_calculator = DistanceCalculator()
    buoy_pixel_x, buoy_pixel_y = distance_calculator.findBuoyPixels()
    disparity_of_buoy = distance_calculator.getDisparityValue(buoy_pixel_x, buoy_pixel_y)
    distance_to_buoy = distance_calculator.getDistance(disparity_of_buoy)

    #Get a reading from airmar
    real_bearing_reading_from_airmar = 13
    get_latitude_from_airmar = 21
    get_longitude_from_airmar = 12

    calculated_bearing_to_buoy = distance_calculator.getBearingFromxPixel(buoy_pixel_x, real_bearing_reading_from_airmar)

    estimated_gps_location_of_buoy = \
        distance_calculator.getBuoyGPSLocation(get_latitude_from_airmar, get_longitude_from_airmar, distance_calculator, calculated_bearing_to_buoy)

