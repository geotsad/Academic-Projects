import numpy as np


def fir_conv(
    in_img_array: np.ndarray,
    h: np.ndarray,
    in_origin: np.ndarray = None,
    mask_origin: np.ndarray = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    Implements 2D convolution of an image with a FIR filter mask using zero-padding.
    """

    # Get dimensions of input image and mask
    H, W = in_img_array.shape
    Mh, Mw = h.shape

    # Default input origin is top-left corner (0, 0) if not specified
    if in_origin is None:
        in_origin = np.array([0, 0])

    # Default mask origin is center of the mask
    if mask_origin is None:
        mask_origin = np.array([Mh // 2, Mw // 2])

    # Compute padding values to apply zero-padding
    pad_top = Mh - 1
    pad_bottom = Mh - 1
    pad_left = Mw - 1
    pad_right = Mw - 1

    # Apply symmetric zero-padding to the image to allow full convolution
    padded_img = np.pad(in_img_array,
                        ((pad_top, pad_bottom), (pad_left, pad_right)),
                        mode='constant', constant_values=0)

    # Output image dimensions based on full convolution
    out_H = H + Mh - 1
    out_W = W + Mw - 1
    out_img_array = np.zeros((out_H, out_W), dtype=float)

    # Flip the mask in both directions for proper convolution (not correlation)
    h_flipped = np.flip(h, axis=(0, 1))

    # Perform the 2D convolution operation
    for i in range(out_H):
        for j in range(out_W):
            # Extract image patch of same size as the mask
            region = padded_img[i:i+Mh, j:j+Mw]

            # Compute weighted sum (dot product of flipped mask and region)
            out_img_array[i, j] = np.sum(region * h_flipped)

    # Compute the new origin in the output image
    out_origin = in_origin + mask_origin

    return out_img_array, out_origin