import numpy as np
import cv2 as cv

# The given video and calibration data
video_file = "C:\\Users\\a\\computer-vision-fundamentals\\camera-calibration-learning\\chessboard5.mp4"
# K = np.array(
#     [
#         [1.15422732e03, 0.00000000e00, 6.71627794e02],
#         [0.00000000e00, 1.15391057e03, 3.65805511e02],
#         [0.00000000e00, 0.00000000e00, 1.00000000e00],
#     ]
# )  # Derived from `calibrate_camera.py`
# dist_coeff = np.array(
#     [
#         -0.2852754904152874,
#         0.1016466459919075,
#         -0.0004420196146339175,
#         0.0001149909868437517,
#         -0.01803978785585194,
#     ]
# )

K = np.array(
    [
        [612.26865008, 0.0, 643.2243679],
        [0.0, 611.58145865, 363.62122411],
        [0.0, 0.0, 1.0],
    ],
)  # Derived from `calibrate_camera.py`
dist_coeff = np.array(
    [-0.03120115, 0.13887876, 0.00036394, -0.00187562, -0.13854699],
)

# Open a video
video = cv.VideoCapture(video_file)
assert video.isOpened(), "Cannot read the given input, " + video_file

# Run distortion correction
show_rectify = True
map1, map2 = None, None
while True:
    # Read an image from the video
    valid, img = video.read()
    if not valid:
        break

    # Rectify geometric distortion (Alternative: `cv.undistort()`)
    info = "Original"
    if show_rectify:
        if map1 is None or map2 is None:
            map1, map2 = cv.initUndistortRectifyMap(
                K, dist_coeff, None, None, (img.shape[1], img.shape[0]), cv.CV_32FC1
            )
        img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)
        info = "Rectified"
    cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # Show the image and process the key event
    cv.imshow("Geometric Distortion Correction", img)
    key = cv.waitKey(10)
    if key == ord(" "):  # Space: Pause
        key = cv.waitKey()
    if key == 27:  # ESC: Exit
        break
    elif key == ord("\t"):  # Tab: Toggle the mode
        show_rectify = not show_rectify

video.release()
cv.destroyAllWindows()
