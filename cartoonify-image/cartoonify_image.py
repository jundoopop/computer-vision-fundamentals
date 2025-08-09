import argparse
from pathlib import Path

import cv2
import numpy as np


def cartoonify_image(path: str) -> np.ndarray:
    """Return a cartoonified version of the image at ``path``.

    Parameters
    ----------
    path: str
        Path to the input image.

    Returns
    -------
    np.ndarray
        Cartoonified image.
    """
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon


def main() -> None:
    parser = argparse.ArgumentParser(description="Cartoonify an image")
    parser.add_argument("input_path", help="Path to input image")
    parser.add_argument(
        "-o", "--output", dest="output_path", help="Path to save cartoon image"
    )
    args = parser.parse_args()

    cartoon = cartoonify_image(args.input_path)
    if args.output_path:
        out_path = Path(args.output_path)
        cv2.imwrite(str(out_path), cartoon)
    else:
        cv2.imshow("Cartoon", cartoon)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
