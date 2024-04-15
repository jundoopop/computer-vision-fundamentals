import numpy as np
import cv2 as cv
import json
from pathlib import Path

# The given video and calibration data
cur_path = Path.cwd() / "camera-calibration-learning"
video_file = str(cur_path / "chessboard5.mp4")


json_file_path = str(cur_path / "calibration_results.json")
with open(json_file_path, "r") as f:
    calibration_results = json.load(f)

# Access the camera matrix and distortion coefficients
camera_matrix_data = calibration_results["camera_calibration_results"]["camera_matrix"]
distortion_coefficient_data = calibration_results["camera_calibration_results"][
    "distortion_coefficient"
]

# Convert to NumPy arrays
camera_matrix = np.array(camera_matrix_data)
distortion_coefficient = np.array(distortion_coefficient_data)

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
                camera_matrix,
                distortion_coefficient,
                None,
                None,
                (img.shape[1], img.shape[0]),
                cv.CV_32FC1,
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
