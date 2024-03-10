import cv2 as cv

# import numpy as np

# video source: updated every 6 minutes.
url = "https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.07452.mp4?i=75uuy"

# open the video
cap = cv.VideoCapture(url)

"""
Show the video until the 'esc' key is pressed.
If its pressed, the window will be closed
By space key is pressed, the record mode and preview mode would be switched
The status of the record mode would be shown on the window title
On the right bottom corner, The red circle would be shown.
when the record mode is on
and saved as 'output.mp4' file
"""
# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*"mp4v")
out = cv.VideoWriter("output.mp4", fourcc, 20.0, (640, 480))

record = False

while cap.isOpened():
    ret, frame = cap.read()
    if ret is True:
        # write the frame
        if record:
            out.write(frame)
            cv.circle(
                frame, (570, 430), 10, (0, 0, 255), -1
            )  # Draw a red circle when recording

        cv.imshow("frame", frame)

        key = cv.waitKey(1)
        if key == 27:  # 'esc' key to stop
            break
        elif key == 32:  # 'space' key to switch record mode
            record = not record
            cv.setWindowTitle("frame", f'Record mode: {"ON" if record else "OFF"}')
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()
