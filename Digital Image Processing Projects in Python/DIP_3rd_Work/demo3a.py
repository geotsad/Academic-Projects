import numpy as np
from scipy.io import loadmat
from image_to_graph import image_to_graph
from n_cuts import n_cuts
import matplotlib.pyplot as plt


# Load input images
data = loadmat('dip_hw_3.mat')
img_a = data['d2a'] 
img_b = data['d2b'] 

def main():
    # Loop over both input images
    for i, img in enumerate([img_a, img_b]):
        # Construct affinity graph from image
        affinity = image_to_graph(img)
        
        # Execute clustering for k=2,3,4 (# clusters)
        for k in [2, 3, 4]:
            # Non-recursive normalized cuts
            labels = n_cuts(affinity, k)

            # Reshape labels to image dimensions for visualization
            seg_img = labels.reshape(img.shape[0], img.shape[1])
            
            # Plot and compare the results
            plt.figure(figsize=(10, 5))
            plt.subplot(121)
            plt.imshow(img)
            plt.title(f'Original Image {"A" if i==0 else "B"}')
            plt.axis('off')

            plt.subplot(122)
            plt.imshow(seg_img, cmap='jet')
            plt.title(f'n-cuts Non-recursive (k={k})')
            plt.axis('off')
            plt.savefig(f'demo3a_img{"A" if i==0 else "B"}_k{k}.png', dpi=150, bbox_inches='tight')
            plt.show()

if __name__ == "__main__":
    main()