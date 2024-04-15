import cv2 as cv
import numpy as np

# Assuming the chessboard detection and pose estimation have already been done and we have rvec, tvec


def draw_pyramid_with_rainbow(img, rvec, tvec, camera_matrix, dist_coeffs):
    # Define 3D points for a pyramid (base + apex)
    pyramid_height = 100  # height of the pyramid
    half_base_size = 50  # half the length of the base square

    obj_points = np.array(
        [
            [half_base_size, half_base_size, 0],  # Base right front
            [-half_base_size, half_base_size, 0],  # Base left front
            [-half_base_size, -half_base_size, 0],  # Base left back
            [half_base_size, -half_base_size, 0],  # Base right back
            [0, 0, pyramid_height],  # Top point (apex)
        ],
        dtype=np.float32,
    )

    # Project 3D points to 2D image plane
    img_points, _ = cv.projectPoints(obj_points, rvec, tvec, camera_matrix, dist_coeffs)

    # Map points from float to int
    img_points = np.int32(img_points).reshape(-1, 2)

    # Draw the base in blue
    cv.polylines(img, [img_points[:4]], True, (255, 0, 0), 2)

    # Colors for the pyramid sides - creating a simple rainbow effect
    colors = [
        (255, 0, 0),  # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),  # Green
    ]

    # Draw sides with different colors
    for i in range(4):
        cv.fillConvexPoly(
            img,
            np.array([img_points[i], img_points[(i + 1) % 4], img_points[4]]),
            colors[i],
        )

    return img


def draw_pyramid_outline(img, rvec, tvec, camera_matrix, dist_coeffs, floor):
    # Define 3D points for a pyramid (base + apex)
    pyramid_height = 100  # height of the pyramid
    half_base_size = 50  # half the length of the base square

    obj_points = np.array(
        [
            [4, 2, 0],
            [5, 2, 0],
            [5, 4, 0],
            [4, 4, 0],
            [0, 0, pyramid_height],  # Top point (apex)
        ],
        dtype=np.float32,
    )

    # Project 3D points to 2D image plane
    edges, _ = cv.projectPoints(obj_points, rvec, tvec, camera_matrix, dist_coeffs)
    cv.polylines(img, [np.int32(edges)], True, (255, 0, 0), 2)

    # Map points from float to int
    img_points = np.int32(edges).reshape(-1, 2)

    # Draw the base
    cv.polylines(img, [img_points[:4]], True, (0, 255, 0), 2)  # Green base

    # Draw the edges from the apex to the base
    for i in range(4):
        cv.line(
            img, tuple(img_points[4]), tuple(img_points[i]), (0, 0, 255), 2
        )  # Red edges

    return img


# Usage example (this part should be integrated where you have the camera parameters and video loop logic):
# img = draw_pyramid_outline(img, rvec, tvec, camera_matrix, dist_coeffs)
# cv.imshow


# Usage example (this part should be integrated where you have the camera parameters and video loop logic):
# img = draw_pyramid_with_rainbow(img, rvec, tvec, camera_matrix, dist_coeffs)
# cv.imshow('Pyramid Projection', img)
# cv.waitKey(0)
# cv.destroyAllWindows()
