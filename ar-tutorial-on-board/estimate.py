import numpy as np
import cv2 as cv
import json
import draw_pyramid as pyramids
from pathlib import Path

# The calibration data
json_file_path = str(
    Path.cwd() / "camera-calibration-learning" / "calibration_results.json"
)
with open(json_file_path, "r") as f:
    calibration_results = json.load(f).get("camera_calibration_results")

print(f"calibration_results: {calibration_results}")

# Access the camera matrix and distortion coefficients
camera_pose = np.array(calibration_results.get("camera_matrix"))
print(f"camera pose:\n {camera_pose}")

dist_coeff = np.array(calibration_results.get("distortion_coefficient"))
print(f"dist_coeff: {dist_coeff}")


video_file_path = str(Path.cwd() / "camera-calibration-learning" / "chessboard5.mp4")

board_pattern = (10, 7)
board_cellsize = 0.5
board_criteria = (
    cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK
)

# Open a video
video = cv.VideoCapture(video_file_path)
assert video.isOpened(), "Cannot read the given input, " + video_file_path

pyramid_height = 3 * board_cellsize  # height of the pyramid above the base

# Prepare a 3D box for simple AR
box_floor = board_cellsize * np.array([[3, 2, 0], [5, 2, 0], [5, 4, 0], [3, 4, 0]])
apex = board_cellsize * np.array([(4, 3, -pyramid_height)])

# Prepare 3D points on a chessboard
obj_points = board_cellsize * np.array(
    [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
)


# Run pose estimation
while True:
    # Read an image from the video
    valid, img = video.read()
    if not valid:
        break

    # Estimate the camera pose
    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(
            obj_points,
            img_points,
            camera_pose,
            dist_coeff,
            flags=cv.SOLVEPNP_ITERATIVE,
        )

        # Project the base and apex points
        base_points, _ = cv.projectPoints(
            box_floor, rvec, tvec, camera_pose, dist_coeff
        )
        apex_point, _ = cv.projectPoints(apex, rvec, tvec, camera_pose, dist_coeff)

        # Draw the base of the pyramid
        cv.polylines(img, [np.int32(base_points)], True, (255, 0, 0), 2)

        # Draw a dot at the apex
        cv.circle(img, tuple(np.int32(apex_point).ravel()), 5, (0, 0, 255), 3)

        # Draw lines from each base corner to the apex
        for point in base_points:
            cv.line(
                img,
                tuple(np.int32(point).ravel()),
                tuple(np.int32(apex_point).ravel()),
                (0, 255, 0),
                2,
            )

        # Print the camera position
        R, _ = cv.Rodrigues(rvec)  # Alternative) `scipy.spatial.transform.Rotation`
        p = (-R.T @ tvec).flatten()
        info = f"XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]"
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # Show the image and process the key event
    cv.imshow("Pose Estimation (Chessboard)", img)
    key = cv.waitKey(10)
    if key == ord(" "):
        key = cv.waitKey()
    if key == 27:  # ESC
        break

video.release()
cv.destroyAllWindows()
