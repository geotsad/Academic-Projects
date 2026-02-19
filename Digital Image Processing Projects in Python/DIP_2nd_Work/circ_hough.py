import numpy as np
from scipy.ndimage import maximum_filter


def circ_hough(
    in_img_array: np.ndarray,
    R_max: float,
    dim: np.ndarray,
    V_min: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    Detects circles in a binary edge image using the circular Hough Transform.
    """

    H, W = in_img_array.shape
    R_min = 50  # Set lower bound for radius

    num_a, num_b, num_r = dim

    # Define the discretized parameter space for center coordinates (a, b) and radius r
    a_range = np.linspace(0, H - 1, num_a)
    b_range = np.linspace(0, W - 1, num_b)
    r_range = np.linspace(R_min, R_max, num_r)

    # Initialize 3D accumulator for voting in parameter space
    accumulator = np.zeros((num_a, num_b, num_r), dtype=int)

    # Retrieve coordinates of edge points (non-zero pixels in binary image)
    edge_points = np.argwhere(in_img_array == 1)

    # Uniform sampling of the unit circle
    theta = np.linspace(0, 2 * np.pi, 100, endpoint=False)

    # For each edge point and radius, vote for possible circle centers (a, b)
    for y, x in edge_points:
        for r_idx, r in enumerate(r_range):
            a_vals = y - r * np.cos(theta)
            b_vals = x - r * np.sin(theta)

            # Quantize coordinates to match discretized accumulator space
            a_idx = np.round((a_vals / (H - 1)) * (num_a - 1)).astype(int)
            b_idx = np.round((b_vals / (W - 1)) * (num_b - 1)).astype(int)

            # Keep only valid index pairs inside accumulator bounds
            valid = (a_idx >= 0) & (a_idx < num_a) & (b_idx >= 0) & (b_idx < num_b)
            for ai, bi in zip(a_idx[valid], b_idx[valid]):
                accumulator[ai, bi, r_idx] += 1

    # Optional step: Non-maximum suppression in 3D to localize distinct peaks
    suppressed = maximum_filter(accumulator, size=(7, 7, 3))
    maxima = (accumulator == suppressed) & (accumulator >= V_min)

    # Extract (a, b, r) values corresponding to detected maxima
    detected = np.argwhere(maxima)

    centers = []
    radii = []

    for a_idx, b_idx, r_idx in detected:
        a = a_range[a_idx]
        b = b_range[b_idx]
        r = r_range[r_idx]

        # Optional filtering step to exclude detections near image borders
        # margin_y = H * 0.4
        # margin_x = W * 0.4
        # if a < margin_y or a > H - margin_y or b < margin_x or b > W - margin_x:
        #     continue

        centers.append([a, b])
        radii.append(r)

    print("Max value in accumulator:", np.max(accumulator))

    return np.array(centers, dtype=float), np.array(radii, dtype=float)