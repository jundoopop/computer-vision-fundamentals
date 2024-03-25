import cv2
import numpy as np
from pathlib import Path

# Load the image

pathOfImage = str(Path.cwd() / "cartoonify-image" / "biden.png")
print(f"Path of Image: {pathOfImage}")
img = cv2.imread(pathOfImage)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Apply median blur to reduce noise
gray = cv2.medianBlur(gray, 5)
# Detect edges using adaptive thresholding
edges = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
)
# Convert the image to color
color = cv2.bilateralFilter(img, 9, 300, 300)
# Combine the color image with the edges mask
cartoon = cv2.bitwise_and(color, color, mask=edges)
# Display the cartoon image
cv2.imshow("Cartoon", cartoon)

while True:
    key = cv2.waitKey(0)
    if key == 27:  # 27 is the ASCII value of 'esc'
        break

cv2.destroyAllWindows()
