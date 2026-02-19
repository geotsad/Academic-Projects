import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from image_to_graph import image_to_graph
from n_cuts import n_cuts, calculate_n_cut_value


# Load data
data = loadmat('dip_hw_3.mat')
img_a = data['d2a']
img_b = data['d2b']
names = ['A', 'B']

def main():
    # Process each image
    for i, img in enumerate([img_a, img_b]):
        affinity = image_to_graph(img)

        # One-step normalized cuts (with n_cuts)
        labels = n_cuts(affinity, k=2)
        ncut_val = calculate_n_cut_value(affinity, labels)

        # Reshape labels to image dimensions for visualization
        seg_img = labels.reshape(img.shape[0], img.shape[1])

        print(f"Image {names[i]}: Ncut Value = {ncut_val:.4f}")

        # Visualize one-step n-cuts
        plt.figure(figsize=(10, 5))
        plt.subplot(121)
        plt.imshow(img)
        plt.title(f'Original Image {names[i]}')
        plt.axis('off')

        plt.subplot(122)
        plt.imshow(seg_img, cmap='jet')
        plt.title('One-Step Recursive N-Cuts (k=2)')
        plt.axis('off')

        plt.tight_layout()
        plt.savefig(f'demo3b_img{names[i]}.png')
        plt.show()

if __name__ == "__main__":
    main()