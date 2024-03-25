import cv2 as cv
import numpy as np
from pathlib import Path

# Load the image

pathOfImage = str(Path.cwd() / "cartoonify-image" / "tony.png")
print(f"Path of Image: {pathOfImage}")
img = cv.imread(pathOfImage)

# Convert the image to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# Apply median blur to reduce noise
gray = cv.GaussianBlur(gray, (11, 11), 0)
# Detect edges using adaptive thresholding
edges = cv.adaptiveThreshold(
    gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 21, 2
)


# Convert the image to color
color = cv.bilateralFilter(cv.bilateralFilter(img, 11, 300, 300), 2, 50, 50)
# Combine the color image with the edges mask
cartoon = cv.bitwise_and(color, color, mask=edges)
# Display the cartoon image


# Stack images vertically
edges_3_channels = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
vertical_stack = np.vstack((img, edges_3_channels, color, cartoon))

# cv.imshow("Cartoon", cartoon)
cv.imshow("Principle of Cartoonify", vertical_stack)

while True:
    key = cv.waitKey(0)
    if key == 27:  # 27 is the ASCII value of 'esc'
        break

cv.destroyAllWindows()
