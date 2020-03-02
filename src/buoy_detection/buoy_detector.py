"""
buoy_detector.py
Evan Allen - SailBOT Buoy Detection 2019-2020
Adapted from Wyatt Lansford's test_cameras.py in the sailbot-20 repo.

Lots of utility methods for analyzing images to find buoys.
"""

import cv2
import numpy as np
import pickle


def get_mask(relevance_map, threshold, open_radius, close_radius):
    """
    Generate the binary mask for a given relevance map.

    Inputs:
        relevance_map -- The relevance map to generate a mask for.
        threshold -- The threshold used to decide what pixels are chosen as "on" and which are chosen as "off".
        open_radius -- The radius of the opening kernel used during mask cleaning.
        close_radius -- The radius of the closing kernel used during mask cleaning.

    Returns:
        A mask image of the same dimensions as `relevance_map` with one channel. Values are either 0 or 255.
    """
    _, mask = cv2.threshold(relevance_map, threshold, 255, cv2.THRESH_BINARY)
    mask = clean_mask(mask, open_radius, close_radius)
    return mask


def clean_mask(mask, open_radius, close_radius):
    """
    Execute opening/closing operations on the mask to get rid of small holes / specks in it.

    Inputs:
        mask -- The mask to clean.
        open_radius -- The radius of the opening kernel.
        close_radius -- The radius of the closing kernel.

    Returns:
        The cleaned mask.
    """
    open_kernel = np.ones((open_radius, open_radius), np.uint8)
    close_kernel = np.ones((close_radius, close_radius), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel)
    return mask


def map_func_combined(depth_channels, histogram_3d):
    """
    Defines a map that assigns each pixel in a relevance map a value by looking it up in a 3D histogram with
    axes corresponding to H/S/V channels.
    ** Only works if we're using 3D histograms that contain information for the H/S/V channels combined! **

    Inputs:
        depth_channels -- A list/tuple of length 3 containing the H/S/V values of an input pixel, respectively.
        histogram_3d -- A 3D histogram representing the relevance of each HSV color.

    Returns:
        The resulting relevance map value for that pixel.
    """
    return histogram_3d[depth_channels[0]][depth_channels[1]][depth_channels[2]]


def get_relevance_map(hsv, histogram_3d, blur_ksize):
    """
    Generate a relevance map from an inputted HSV-format image and the histogram previously retrieved during
    initialization.

    Inputs:
        hsv -- The input image, in HSV-format.
        histogram_3d -- The 3D histogram containing relevance values for each HSV color.
        blur_ksize -- The k-parameter for the median blur used to clean the relevance map.

    Returns:
        The relevance map for that input image, in the form of a 1-channel image (uint8) of the same
        dimensions as the input image.
    """

    relevance_map = np.apply_along_axis(map_func_combined, 2, hsv, histogram_3d)
    relevance_map = relevance_map.astype(np.uint8)

    # De-noise
    relevance_map = cv2.medianBlur(relevance_map, blur_ksize)

    return relevance_map


def get_histogram(histogram_path):
    """
    Load the histogram(s) from the stored file ("buoy_histogram.pickle").

    Returns:
        The loaded histogram.
    """
    # The stored histogram is the only element in a tuple. This is because we used to have an option to pass
    # multiple histograms.
    # TODO Store the histogram by itself and don't wrap it in a tuple.
    with open(histogram_path, "rb") as pickle_file:
        return pickle.load(pickle_file)[0]


def process_image(image, threshold, histogram_3d, open_radius, close_radius, blur_ksize):
    """
    Convert the image to HSV, find the buoy-colored pixels, and draw contours.

    Inputs:
        image -- The image to analyze.
        threshold -- The threshold used to create a binary mask from the relevance map.
        histogram_3d -- The 3D histogram containing relevance values for each HSV color.
        open_radius -- The radius of the opening kernel for mask cleaning.
        close_radius -- The radius of the closing kernel for mask cleaning.
        blur_ksize -- The k-parameter for the median blur used for cleaning the relevance map.

    Returns:
        A tuple (relevance_map, mask) with those elements.
    """
    # Convert image to HSV, and find/clean mask with buoy-colored pixels.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    relevance_map = get_relevance_map(hsv, histogram_3d, blur_ksize)

    mask = get_mask(relevance_map, threshold, open_radius, close_radius)

    return relevance_map, mask
