# Requirements for Calibration:
-   A stereo set of images from a pair of LEFT/RIGHT cameras, which are each as close to parallel as possible
    (important!).
-   Each image must contain a chessboard calibration pattern visible to BOTH cameras.
-   The images must be stored in `base_path/LEFT` and `base_path/RIGHT`, respectively, where base_path is some
    path provided to the Calibrator class. Each image in a LEFT/RIGHT pair should have the same base name so that
    the Calibrator can associate them with one another.
-   For accurate calibration, the chessboard pattern must be printed extremely accurately
    (laser-printer recommended).

# Background:
-   Stereo cameras are useful because they allow us to judge depth by comparing the locations of an object in images
    taken simultaneously by two side-by-side cameras, just like how we can judge depth with our two eyes.

-   To calculate this depth, though, we need to know exactly how the two cameras are:
    1. Positioned (i.e., where they ARE) relative to each other, and how they're
    2. Oriented (i.e., where they're LOOKING) relative to each other.
    -   **DEFN**: This data is called the stereo cameras' **EXTRINSIC PARAMETERS**.
    -   **DEFN**: Extrinsic parameters are calculated through **STEREO CALIBRATION**.

-   In addition, each camera has certain unique properties related to its focal length and distortion that we must
    know.
    -   **DEFN**: These properties are called **INTRINSIC PARAMETERS**, and are specific to each INDIVIDUAL camera.

-   Consider a point viewed by a camera.
    -   **DEFN**: Its 3D coordinates in the real world are referred to as an **OBJECT POINT**.
    -   **DEFN**: Its 2D coordinates projected onto the image plane are referred to as an **IMAGE POINT**.

-   We use a well-defined pattern like a chessboard to determine these intrinsic and extrinsic parameters by
    associating object points (which we know *IN ADVANCE*, since we know the size of the chessboard) with image points
    in each camera, and comparing the two sets of image points between the cameras.
    -   To elaborate: we know the object points of the chessboard in advance because we _set our coordinate system_
        such that the chessboard is the XY-plane with the origin at one corner and the axes along the edges.
        With this view, it's like the chessboard is stationary and we're moving the cameras (even if we're not).

-   When we want to compare the images from each camera to determine the depth of a point in the image, it's important
    that the image planes of each camera lie in the same plane (which we achieve if the cameras are EXACTLY parallel).
    This is difficult to do in real life, though, so we can slightly transform the images so that it's _as if_ they
    were taken from two cameras that were exactly parallel.
    -   **DEFN**: This process of transforming images so they seem like they were taken from parallel cameras is called
              **STEREO RECTIFICATION**.
              Further reading:  http://people.scs.carleton.ca/~c_shu/Courses/comp4900d/notes/rectification.pdf

# HOW IT WORKS:
1.  **SETUP & DATA COLLECTION**
    1.  Set up the cameras next to each other so that they are _as parallel as possible_ and measure the
        physical distance between them in meters (this is called the BASELINE, which is used in other files).
        
        *DO NOT MOVE THE CAMERAS*! If you do, you'll have to calibrate again.
    
    2.  Take a bunch of pictures of a chessboard calibration pattern with both the left and right cameras
        at the same time, storing each pair in the folders specified above.

2.  **CORNER IDENTIFICATION**
    3.  Once you have the data, the Calibrator will enumerate through each set of images trying to identify
        the image points of each of the chessboard's internal corners.
        a.  If the Calibrator cannot identify all the expected corners in an image, it (and its corresponding pair
            image from the other camera) are removed.
    4.  Then the Calibrator refines its image points to a sub-pixel level using `cv2.cornerSubPix`.

3.  **INDIVIDUAL CAMERA CALIBRATION**
    5.  The Calibrator then determines intrinsic parameter matrices for the left and right cameras (as well
        as their distortion coefficients) using these image point / object point correspondence data.

4.  **STEREO CAMERA CALIBRATION**
    6.  Then, the Calibrator determines the rotation matrix and translation vector that transform points from
        the first camera's view to the second's. These form the extrinsic parameters.

5.  **STEREO RECTIFICATION**
    7.  Using the image point / object point data as well as the intrinsic parameters of each camera, the Calibrator
        calculates a set of RECTIFICATION and PROJECTION matrices that allow us to transform image points viewed by
        either camera into image points on a common plane, which allows us to take disparity measurements
        (how far apart two corresponding image points are between cameras) and consequently depth measurements.
        -   Because this process provides us matrices to transform images from both cameras, it also gives us
            data on which part of those transformed images are actually useful (called REGIONS OF INTEREST, or ROI).
        -   In addition, it also provides a Q-MATRIX, which converts points in image space (along with a disparity)
            to 3D points in physical space.

6.  **SAVING**
    8.  Finally, the data is saved. Calibration data that can be used for depth calculation is stored in
        "stereo_calibration.npz" at some desired location, and the projection/rectification matrices themselves
        are stored in "projection_matrices.npz" at some desired location.