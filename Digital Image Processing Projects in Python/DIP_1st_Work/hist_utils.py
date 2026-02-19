import numpy as np


def calculate_hist_of_img(
    img_array: np.ndarray,
    return_normalized: bool
) -> dict:
    """
    Calculates the histogram (counts ή normalized) of a grayscale image [0, 1]
    """
    # Convert the 2D array to 1D (easier maths on list)
    flat = img_array.flatten() 

    # Returns the unique values of brigthness levels and the number of pixels per level
    levels, num_of_pixels = np.unique(flat, return_counts=True) 

    if return_normalized:
        num_of_pixels = num_of_pixels / flat.size
    return dict(zip(levels, num_of_pixels)) # With 'zip' we create the key-value pairs of the dictionary


def apply_hist_modification_transform(
    img_array: np.ndarray,
    modification_transform: dict
) -> np.ndarray:
    """
    Efficiently applies mapping fi -> gi to the input image using numpy vectorization.
    Assumes img_array values are already between 0 and 1.
    """
    # Convert the 2D array to 1D
    flat_img = img_array.flatten()

    # Create array of input image's brightness levels(fi) and their mapped values (output - gi)
    fi_levels = np.array(list(modification_transform.keys()))
    gi_levels = np.array(list(modification_transform.values()))

    # Create a lookup mechanism (like dict) using numpy's argsort (assumes keys are sorted)
    sort_idx = np.argsort(fi_levels) # returns the indices of the fi levels
    fi_sorted = fi_levels[sort_idx]
    gi_sorted = gi_levels[sort_idx]

    # Use searchsorted for fast indexing (finds in which index would be placed each value of flat_img)
    indices = np.searchsorted(fi_sorted, flat_img)
    indices = np.clip(indices, 0, len(gi_sorted) - 1)

    # Maps the appropriate fi to the gi level
    mapped_flat = gi_sorted[indices]

    return mapped_flat.reshape(img_array.shape)