import numpy as np
from fir_conv import fir_conv


def sobel_edge(
    in_img_array: np.ndarray,
    thres: float
) -> np.ndarray:
    """
    Applies the Sobel operator to detect edges in a grayscale image.
    """

    # Define Sobel masks to approximate first-order derivatives
    # Gx: for horizontal gradient (changes along columns)
    # Gy: for vertical gradient (changes along rows)
    Gx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=float)

    Gy = np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ], dtype=float)

    # Apply convolution of image with Sobel masks using FIR filtering
    gx, _ = fir_conv(in_img_array, Gx)  # Horizontal gradient
    gy, _ = fir_conv(in_img_array, Gy)  # Vertical gradient

    # Compute the gradient magnitude at each pixel
    g = np.sqrt(gx**2 + gy**2)

    # Threshold the gradient magnitude to produce binary edge map
    out_img_array = (g > thres).astype(int)

    return out_img_array