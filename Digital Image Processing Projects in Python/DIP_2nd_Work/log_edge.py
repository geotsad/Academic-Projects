import numpy as np
from fir_conv import fir_conv
from scipy.ndimage import gaussian_filter


def log_edge(in_img_array: np.ndarray, epsilon: float, pattern: int) -> np.ndarray:
    """
    Detect edges using Laplacian of Gaussian (LoG) method and pattern-based zero-crossing detection.

    Parameters:
    - in_img_array: Input grayscale image (2D numpy array)
    - epsilon: Minimum difference between regional means for validation
    - pattern: Detection pattern to use (1=simple, 2=symmetric, 3=grid)

    Returns:
    - Binary image (edges marked as 1)
    """
    # Define fixed 5x5 LoG mask
    log_mask = np.array([
        [ 0,  0, -1,  0,  0],
        [ 0, -1, -2, -1,  0],
        [-1, -2, 16, -2, -1],
        [ 0, -1, -2, -1,  0],
        [ 0,  0, -1,  0,  0]
    ], dtype=float)

    # Convolve input image with LoG mask using FIR convolution
    log_result, _ = fir_conv(in_img_array, log_mask)
    out_img_array = np.zeros_like(log_result, dtype=int)
    H, W = log_result.shape

    # Pattern 1: Basic zero-crossing detection in 3x3 neighborhood
    if pattern == 1:
        for i in range(1, H - 1):
            for j in range(1, W - 1):
                patch = log_result[i-1:i+2, j-1:j+2]
                center = log_result[i, j]
                # If any neighbor has opposite sign, mark as edge
                if np.any(patch * center < 0):
                    out_img_array[i, j] = 1

    # Pattern 2: Directional zero-crossing detection with symmetric pixel pairs
    elif pattern == 2:
        # Smooth input before applying LoG to reduce noise
        smoothed = gaussian_filter(in_img_array, sigma=1.0)
        log_result, _ = fir_conv(smoothed, log_mask)

        for i in range(1, H - 1):
            for j in range(1, W - 1):
                # Check opposite symmetric directions 
                pairs = [
                    (log_result[i-1, j], log_result[i+1, j]),      # vertical
                    (log_result[i, j-1], log_result[i, j+1]),      # horizontal
                    (log_result[i-1, j-1], log_result[i+1, j+1]),  # diagonal \
                    (log_result[i-1, j+1], log_result[i+1, j-1])   # diagonal /
                ]
                # Count how many directions indicate zero-crossing with sufficient contrast
                count = sum(1 for p1, p2 in pairs if p1 * p2 < 0 and abs(p1 - p2) > epsilon)
                if count >= 3:
                    out_img_array[i, j] = 1

    # Pattern 3: Grid-based strict zero-crossing detection in 5x5 neighborhood
    else:
         # This pattern checks opposite regions in a 5x5 window to validate edge consistency
        for i in range(2, H - 2):
            for j in range(2, W - 2):

                # Horizontal pattern check: left vs right columns
                if log_result[i-1, j-1] * log_result[i-1, j+1] < 0:
                    left = [(i, j-1), (i+1, j-1), (i-2, j-1), (i+2, j-1),
                            (i-1, j-2), (i, j-2), (i+1, j-2), (i-2, j-2), (i+2, j-2)]
                    right = [(i, j+1), (i+1, j+1), (i-2, j+1), (i+2, j+1),
                             (i-1, j+2), (i, j+2), (i+1, j+2), (i-2, j+2), (i+2, j+2)]
                    if all(log_result[i-1, j-1] * log_result[x, y] > 0 for x, y in left) and \
                       all(log_result[i-1, j+1] * log_result[x, y] > 0 for x, y in right):
                        mean_left = np.mean([log_result[x, y] for x, y in [(i-1, j-1)] + left])
                        mean_right = np.mean([log_result[x, y] for x, y in [(i-1, j+1)] + right])
                        if abs(mean_left - mean_right) > epsilon:
                            out_img_array[i, j] = 1

                # Vertical pattern check: top vs bottom rows
                if log_result[i-1, j-1] * log_result[i+1, j-1] < 0:
                    top = [(i-1, j), (i-1, j+1), (i-1, j-2), (i-1, j+2),
                           (i-2, j-1), (i-2, j), (i-2, j+1), (i-2, j-2), (i-2, j+2)]
                    bottom = [(i+1, j), (i+1, j+1), (i+1, j-2), (i+1, j+2),
                              (i+2, j-1), (i+2, j), (i+2, j+1), (i+2, j-2), (i+2, j+2)]
                    if all(log_result[i-1, j-1] * log_result[x, y] > 0 for x, y in top) and \
                       all(log_result[i+1, j-1] * log_result[x, y] > 0 for x, y in bottom):
                        mean_top = np.mean([log_result[x, y] for x, y in [(i-1, j-1)] + top])
                        mean_bottom = np.mean([log_result[x, y] for x, y in [(i+1, j-1)] + bottom])
                        if abs(mean_top - mean_bottom) > epsilon:
                            out_img_array[i, j] = 1

                # Diagonal pattern: top-left vs bottom-right
                if log_result[i-1, j-1] * log_result[i+1, j+1] < 0:
                    tl = [(i, j-1), (i-1, j), (i-2, j-2), (i-2, j-1), (i-2, j),
                          (i-1, j-2), (i, j-2)]
                    br = [(i, j+1), (i+1, j), (i+2, j+2), (i+2, j+1), (i+2, j),
                          (i+1, j+2), (i, j+2)]
                    if all(log_result[i-1, j-1] * log_result[x, y] > 0 for x, y in tl) and \
                       all(log_result[i+1, j+1] * log_result[x, y] > 0 for x, y in br):
                        mean_tl = np.mean([log_result[x, y] for x, y in [(i-1, j-1)] + tl])
                        mean_br = np.mean([log_result[x, y] for x, y in [(i+1, j+1)] + br])
                        if abs(mean_tl - mean_br) > epsilon:
                            out_img_array[i, j] = 1

                # Diagonal pattern: bottom-left vs top-right
                if log_result[i+1, j-1] * log_result[i-1, j+1] < 0:
                    bl = [(i, j-1), (i+1, j), (i+2, j-2), (i+2, j-1), (i+2, j),
                          (i+1, j-2), (i, j-2)]
                    tr = [(i-1, j), (i, j+1), (i-2, j+2), (i-2, j+1), (i-2, j),
                          (i-1, j+2), (i, j+2)]
                    if all(log_result[i+1, j-1] * log_result[x, y] > 0 for x, y in bl) and \
                       all(log_result[i-1, j+1] * log_result[x, y] > 0 for x, y in tr):
                        mean_bl = np.mean([log_result[x, y] for x, y in [(i+1, j-1)] + bl])
                        mean_tr = np.mean([log_result[x, y] for x, y in [(i-1, j+1)] + tr])
                        if abs(mean_bl - mean_tr) > epsilon:
                            out_img_array[i, j] = 1

    return out_img_array
