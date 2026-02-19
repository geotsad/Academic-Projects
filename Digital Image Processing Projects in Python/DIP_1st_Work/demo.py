'''
Demo script to visualize and compare the effects of histogram equalization 
and histogram matching using three different algorithmic approaches:
greedy, non-greedy, and post-disturbance. 
For each method, the input image is processed and displayed alongside 
its histogram and the result.

'''

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from hist_utils import calculate_hist_of_img
from hist_modif import perform_hist_eq, perform_hist_matching

# Read and preprocess input image: 
# grayscale conversion and normalization to [0, 1].
filename1 = "hw1_images/input_img.jpg"
input_img = Image.open(fp=filename1)
bw_input_img = input_img.convert("L")
input_img_array = np.array(bw_input_img).astype(float) / 255.0

# Read and preprocess reference image: 
# grayscale conversion and normalization to [0, 1].
filename2 = "hw1_images/ref_img.jpg"
ref_img = Image.open(fp=filename2)
bw_ref_img = ref_img.convert("L")
ref_img_array = np.array(bw_ref_img).astype(float) / 255.0


def show_side_by_side_plot(
    input_img_array: np.ndarray,
    ref_img_array: np.ndarray,
    mode: str,
    operation_type: str = "equalization", 
    save=False
):
    if operation_type == "equalization":
        processed = perform_hist_eq(input_img_array, mode=mode)
        title = f"Histogram Equalization - Mode: {mode}"

        # Prepare histogramms
        hist_input = calculate_hist_of_img(input_img_array, return_normalized=False)
        hist_proc = calculate_hist_of_img(processed, return_normalized=False)

        # Plot
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(title, fontsize=16)

        axs[0, 0].imshow(input_img_array, cmap="gray", vmin=0, vmax=1)
        axs[0, 0].set_title("Original Image")
        axs[0, 0].axis("off")

        axs[0, 1].imshow(processed, cmap="gray", vmin=0, vmax=1)
        axs[0, 1].set_title("Processed Image")
        axs[0, 1].axis("off")

        axs[1, 0].bar(hist_input.keys(), hist_input.values(), width=0.0025)
        axs[1, 0].set_title("Original Histogram")
        axs[1, 0].set_xlim(0, 1)

        axs[1, 1].bar(hist_proc.keys(), hist_proc.values(), width=0.0025)
        axs[1, 1].set_title("Processed Histogram")
        axs[1, 1].set_xlim(0, 1)

    elif operation_type == "matching":
        processed = perform_hist_matching(input_img_array, ref_img_array, mode=mode)
        title = f"Histogram Matching - Mode: {mode}"

        hist_input = calculate_hist_of_img(input_img_array, return_normalized=False)
        hist_proc = calculate_hist_of_img(processed, return_normalized=False)
        hist_ref = calculate_hist_of_img(ref_img_array, return_normalized=False)

        fig, axs = plt.subplots(3, 2, figsize=(12, 10))
        fig.suptitle(title, fontsize=16)

        axs[0, 0].imshow(input_img_array, cmap="gray", vmin=0, vmax=1)
        axs[0, 0].set_title("Original Image")
        axs[0, 0].axis("off")

        axs[0, 1].bar(hist_input.keys(), hist_input.values(), width=0.0025)
        axs[0, 1].set_title("Original Histogram")
        axs[0, 1].set_xlim(0, 1)

        axs[1, 0].imshow(ref_img_array, cmap="gray", vmin=0, vmax=1)
        axs[1, 0].set_title("Reference Image")
        axs[1, 0].axis("off")

        axs[1, 1].bar(hist_ref.keys(), hist_ref.values(), width=0.0025)
        axs[1, 1].set_title("Reference Histogram")
        axs[1, 1].set_xlim(0, 1)

        axs[2, 0].imshow(processed, cmap="gray", vmin=0, vmax=1)
        axs[2, 0].set_title("Processed Image")
        axs[2, 0].axis("off")

        axs[2, 1].bar(hist_proc.keys(), hist_proc.values(), width=0.0025)
        axs[2, 1].set_title("Processed Histogram")
        axs[2, 1].set_xlim(0, 1)

    else:
        raise ValueError("operation_type must be 'equalization' or 'matching'")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    if save:
        filename = f"{operation_type}_{mode}.png"
        plt.savefig(filename)
        print(f"Saved as {filename}")
    else:
        plt.show()


def main():
    for mode in ["greedy", "non-greedy", "post-disturbance"]:
        print(f"\n== EQUALIZATION - {mode} ==")
        show_side_by_side_plot(input_img_array, ref_img_array, mode, operation_type="equalization", save=True)

        print(f"\n== MATCHING - {mode} ==")
        show_side_by_side_plot(input_img_array, ref_img_array, mode, operation_type="matching", save=True)

if __name__ == "__main__":
    main()