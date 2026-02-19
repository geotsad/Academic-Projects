import numpy as np
from hist_utils import(
    calculate_hist_of_img,
    apply_hist_modification_transform)


def perform_hist_modification(
        img_array: np.ndarray, 
        hist_ref: dict, mode: str
) -> np.ndarray:
    '''
    Applies histogram modification to the image, based on the given algorithm.
    '''
    if mode == "greedy":
        modif_transform = greedy_hist_approximation(img_array, hist_ref)
        modified_img = apply_hist_modification_transform(img_array, modif_transform)
    elif mode == "non-greedy":
        modif_transform = non_greedy_hist_approximation(img_array, hist_ref)
        modified_img = apply_hist_modification_transform(img_array, modif_transform)
    elif mode == "post-disturbance":
        mod_transform, disturbed = post_disturbance_hist_approximation(img_array, hist_ref)
        modified_img = apply_hist_modification_transform(disturbed, mod_transform)
    else:
        raise ValueError("Invalid mode. Accepted: 'greedy', 'non-greedy', 'post-disturbance'")

    return modified_img


def perform_hist_eq(
        img_array: np.ndarray, 
        mode: str
) -> np.ndarray:
    '''
    Performs histogram equalization using the selected mode, 
    transforming the image such that its histogram approximates 
    a uniform distribution across the output intensity levels.
    '''
    Lg = len(np.unique(img_array))  # number of output levels
    output_levels = np.linspace(0, 1, Lg)
    # output_levels = np.round(np.linspace(0, 1, Lg), 5)
    hist_ref = {level: 1 / Lg for level in output_levels}

    return perform_hist_modification(img_array, hist_ref, mode)


def perform_hist_matching(
    img_array: np.ndarray,
    img_array_ref: np.ndarray,
    mode: str
) -> np.ndarray:
    '''
    Applies histogram matching of img_array,
    in order to approximate the histogram of img_array_ref.
    '''
    hist_ref = calculate_hist_of_img(img_array_ref, return_normalized = True)
    return perform_hist_modification(img_array, hist_ref, mode)


def greedy_hist_approximation(img_array: np.ndarray, hist_ref: dict) -> dict:
    '''
    Builds a mapping fi → gi so that the histogram of the input image 
    approximates the reference histogram using a greedy allocation strategy.
    '''
     # If hist_ref is normalized (values in [0, 1]), convert to absolute pixel counts
    if max(hist_ref.values()) <= 1.0:
        N = img_array.size
        hist_ref = {k: v * N for k, v in hist_ref.items()}

    # Compute the histogram of the input image (not normalized)
    hist_input = calculate_hist_of_img(img_array, return_normalized = False)
    
    modification_transform = {} # Final mapping from input levels (fi) to output levels (gi)
    modification_hist = {}      # Tracks how much of each gi level has been filled
    used_keys = set()           # Keeps track of which fi levels have already been mapped

    # Greedy rule: assign fi levels to gi levels in order, until each gi is "full"
    for key_ref in sorted(hist_ref):
        modification_hist[key_ref] = 0
        for key_input in sorted(hist_input):
            if modification_hist[key_ref] >= hist_ref[key_ref]:
                break # Stop when this gi level is filled
            elif key_input not in used_keys:
                modification_hist[key_ref] += hist_input[key_input]
                modification_transform[key_input] = key_ref
                used_keys.add(key_input)

    return modification_transform


def non_greedy_hist_approximation(img_array: np.ndarray, hist_ref: dict) -> dict:
    '''
    Builds a mapping fi → gi such that the input image's histogram 
    approximates the reference histogram using a more conservative rule:
    it avoids overfilling each gi level early unless necessary.
    '''
    # If hist_ref is normalized (values in [0, 1]), convert to absolute pixel counts
    if max(hist_ref.values()) <= 1.0: 
        N = img_array.size
        hist_ref = {k: v * N for k, v in hist_ref.items()}

    # Compute the (non-normalized) histogram of the input image
    hist_input = calculate_hist_of_img(img_array, False)

    modification_transform = {} # Final mapping from input levels (fi) to output levels (gi)
    modification_hist = {}      # Tracks how much of each gi level has been filled
    used_keys = set()           # Keeps track of which fi levels have already been mapped

    # Non-greedy rule: only assign if the fi value meaningfully 
    # contributes or if the gi bucket is still empty
    for key_ref in sorted(hist_ref):
        modification_hist[key_ref] = 0
        for key_input in sorted(hist_input):
            if key_input in used_keys:
                continue
            deficiency = hist_ref[key_ref] - modification_hist[key_ref]
            if deficiency >= hist_input[key_input] / 2 or modification_hist[key_ref] == 0:
                modification_hist[key_ref] += hist_input[key_input]
                modification_transform[key_input] = key_ref
                used_keys.add(key_input)
            else:
                break # Move to the next gi level

    return modification_transform


def post_disturbance_hist_approximation(img_array: np.ndarray, hist_ref) -> tuple:
    '''
    Applies histogram modification using the greedy strategy **after adding noise** 
    to the input image.
    Returns:
        mapping (dict): mapping fi → gi based on the disturbed image.
        disturbed_img_array (ndarray): the noise-perturbed version of img_array.
    '''
    # Find the unique brigthness levels in the input image
    f_levels = np.unique(img_array)

    # Compute the intensity step (quantization bin width)
    d = f_levels[1] - f_levels[0] if len(f_levels) > 1 else 1e-5

    # Add uniform random noise in range [-d/2, d/2] to each pixel
    # to disperse concentrated input levels, allowing better distribution 
    # across output levels during mapping.
    noise = np.random.uniform(-d/2, d/2, size=img_array.shape)
    disturbed_img_array = np.clip(img_array + noise, 0, 1) 

    # Apply greedy histogram approximation to the disturbed image
    mapping = greedy_hist_approximation(disturbed_img_array, hist_ref)

    return mapping, disturbed_img_array