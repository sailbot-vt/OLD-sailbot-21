Steps:

1. image_capture.py

Capture as many images as is feasible of the checkerboard pattern in various orientations.
Tilt in all 3 axis directions, and do your best to make sure the whole clipboard is visible in both cameras.

    Tips:
        ALWAYS HAVE GOOD LIGHTING
        CHECKERBOARD MUST BE COMPLETELY FLAT (but can rotate in any direction). Tape the checkerboard to a clipboard if possible (one is found in bay)
        The whole checkerboard must be present in both cameras
        Try to take pictures where the checkerboard is along the edges and corners of the images (while still having the full checkerboard in the images).
            This is where most of the distortion of the image occurs
        Taking the same picture more than once will not help accuracy and will only slow down calibration
        Taking a picture where the checkerboard is in the same spot but rotated will help

2. calibration.py

Run calibration and wait for it to finish. 
If you have over 100 images, it may take quite awhile but the calibration will be more accurate.


3. Distance_Calculator.py

This class is the user facing class, use its method's in order to calculate the GPS location of a buoy. 
An example is found in Example_Usage.py