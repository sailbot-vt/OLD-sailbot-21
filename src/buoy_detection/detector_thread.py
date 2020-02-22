from threading import Thread

from pubsub import pub

import src.buoy_detection.Distance_Calculator as dc
import src.buoy_detection.buoy_detector as bd
from src.tracking.classification_types import ObjectType
import time
import logging
import cv2


def find_object_centers(contours):
    """Finds the centers of objects given a list of their contours.

    Inputs:
        contours -- A list of the object contours, as returned from cv2.findContours.

    Returns:
        A list of the center-coordinates of the objects (length = len(contours)), each in the form
        (x_coordinate, y_coordinate).
    """
    # Code adapted from https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
    # See https://docs.opencv.org/3.4/d8/d23/classcv_1_1Moments.html#a42016f07a907b360d499ed56239eb245
    # for details on moments data structure (what the 'm10' means, etc.)
    object_centers = []
    for contour in contours:
        moments = cv2.moments(contour)
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        object_centers.append((cx, cy))

    return object_centers


def stretch_bounds(bounds, new_val):
    """Stretches a list of bounds based on a new input value.

    Inputs:
        bounds -- A list containing two entries representing the minimum and maximum of some range.
        new_val -- A new value used to update bounds.

    Returns:
        An updated version of bounds "stretched" to accommodate new_val if it isn't already in the range
        specified by bounds.
        For example, if bounds = [3, 5] and new_val = 7, then this function returns [3, 7].
        If bounds = [3, 5] and new_val = 4, then this function returns [3, 5] (no stretching needed).
    """
    stretched = bounds.copy()
    if new_val < stretched[0]:
        stretched[0] = new_val
    if new_val > stretched[1]:
        stretched[1] = new_val

    return stretched


class DetectorThread(Thread):
    def __init__(self, master_config, boat):
        super().__init__()
        self.distance_calculator = dc.DistanceCalculator(master_config)
        self.buoy_location = None
        self.boat = boat

        config = master_config["buoy_detector"]
        self.threshold = config["threshold_pct"] * 255
        self.open_radius = config["open_radius"]
        self.close_radius = config["close_radius"]
        self.blur_ksize = config["blur_ksize"]

        histogram_path = config["histogram_path"]
        self.histogram = bd.get_histogram(histogram_path)

        self.update_interval = config["update_interval"]
        self.running = False

    def get_camera_heading(self):
        """Returns the heading of the camera.
        Placeholder for now until we actually have this functionality - for
        now, we'll just assume the camera heading is 0 degrees.
        (The placeholder can be static, but we're keeping it an object
        method for now since we'll likely use a property of the boat
        to find the camera heading.)

        Returns:
            The camera heading (not implemented yet, so 0 for now).
        """
        return 0

    def handle_contours(self, contours, disparity_frame):
        """Analyzes contours found from the mask.

        Inputs:
            contours -- A contours object from cv2.findContours.
            disparity_frame -- A disparity map, from depth_map_calculator.calculate_depth_map.

        Side Effects:
            If objects are detected in the frame, send a message with information on the detected objects'
            ranges and bearings out for tracking to handle.
        """
        if len(contours) > 0:
            buoy_centers = find_object_centers(contours)

            # Of the form [(rng, bearing, ObjectType.BUOY)...]
            epoch_frame = []
            rng_bounds = []
            bearing_bounds = []

            for (center_x, center_y) in buoy_centers:
                bearing = self.distance_calculator.get_bearing_from_pixel(center_x, self.get_camera_heading())
                disparity = dc.get_disparity_value(disparity_frame, center_x, center_y)
                rng = self.distance_calculator.get_distance(disparity)

                buoy_tuple = (rng, bearing, ObjectType.BUOY)
                epoch_frame.append(buoy_tuple)

                if len(rng_bounds) == 0:
                    rng_bounds = [rng, rng]
                    bearing_bounds = [bearing, bearing]
                else:
                    rng_bounds = stretch_bounds(rng_bounds, rng)
                    bearing_bounds = stretch_bounds(bearing_bounds, bearing)

            frame_bounds = (rng_bounds, bearing_bounds)

            pub.sendMessage("object(s) detected", epoch_frame=epoch_frame, frame_bounds=frame_bounds)

    def quit(self):
        """Quit the run method.

        Side Effects:
            Sets the self.running field to False and quits the continuous buoy
            detection thread.
        """
        self.running = False

    def run(self):
        """Continuously checks for a buoy.
        Do not directly call! Use the Thread superclass's
        start() method so this doesn't run synchronously."""
        self.running = True
        last_time = time.time()

        while self.running:

            # Enforce minimum update interval.
            if time.time() - last_time < self.update_interval:
                continue

            try:
                left_frame, disparity_frame = self.distance_calculator.depth_map_calculator.calculate_depth_map()
            except Exception:
                logging.getLogger().error("Couldn't calculate depth map!", exc_info=True)
                continue

            _, mask = bd.process_image(left_frame, self.threshold, self.histogram,
                                       self.open_radius, self.close_radius, self.blur_ksize)

            # Finding the external contours of our mask allows us to separate each individual detection.
            # For the purposes of our system, connected pixels in the mask are one detection.
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.handle_contours(contours, disparity_frame)

            last_time = time.time()

