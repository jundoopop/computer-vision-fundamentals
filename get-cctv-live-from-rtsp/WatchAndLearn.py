import cv2 as cv
from datetime import datetime
import time
import pytz


def on_trackbar(val):
    global playback_speed
    val = max(1, val)
    playback_speed = val / 10.0


def mouse_click(event, x, y, flags, param):
    global hist_eq, record
    if (
        event == cv.EVENT_LBUTTONDOWN and not record
    ):  # Only allow toggling if not currently recording
        hist_eq = not hist_eq


url = "https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.07452.mp4?i=75uuy"
cap = cv.VideoCapture(url)

if not cap.isOpened():
    print("Error opening video stream or file")
    exit(1)

record = False
out = None
last_blink_time = time.time()
blink_interval = 0.5
blink_on = False
hist_eq = False  # Initialize histogram equalization flag as False

cv.namedWindow("frame")
cv.createTrackbar("Speed", "frame", 10, 20, on_trackbar)
cv.setMouseCallback("frame", mouse_click)  # Set mouse callback

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue

    if hist_eq:
        # Convert to HSV, equalize the V channel, and convert back to BGR
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        hsv[:, :, 2] = cv.equalizeHist(hsv[:, :, 2])
        frame = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

    if record and time.time() - last_blink_time >= blink_interval:
        blink_on = not blink_on
        last_blink_time = time.time()

    if record and blink_on:
        cv.circle(frame, (250, 250), 20, (0, 0, 255), -1)

    if record:
        out.write(frame)

    cv.imshow("frame", frame)

    key = cv.waitKey(max(1, int(30 / playback_speed))) & 0xFF
    if key == 27:
        break
    elif key == 32:
        record = not record
        if record:

            # Get current time in London Oxford timezone
            now = datetime.now(pytz.timezone("Europe/London")).strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            # Check if video is equalised or normal
            if hist_eq:
                filename = f"London Oxford Circle - equalised - {now}.mp4"
            else:
                filename = f"London Oxford Circle - original - {now}.mp4"

            out = cv.VideoWriter(
                filename,
                cv.VideoWriter_fourcc(*"mp4v"),
                20.0,
                (int(cap.get(3)), int(cap.get(4))),
            )
            last_blink_time = time.time()
        else:
            if out is not None:
                out.release()
                out = None
                print("Recording stopped and saved.")

if out is not None:
    out.release()
cap.release()
cv.destroyAllWindows()
