import numpy as np
from scipy.io import loadmat
from image_to_graph import image_to_graph
from n_cuts import n_cuts_recursive
import matplotlib.pyplot as plt


# Load data
data = loadmat('dip_hw_3.mat')
img_a = data['d2a']
img_b = data['d2b'] 

T1 = 5   # Minimum cluster size threshold
T2 = 0.2  # Maximum Ncut value threshold 
# T2 = 0.99 # Much better results especially for d2b

def main():
    for i, img in enumerate([img_a, img_b]):
        affinity = image_to_graph(img)

        # Recursive normalized cuts
        labels = n_cuts_recursive(affinity, T1, T2)

        # Reshape labels to image dimensions for visualizations
        seg_img = labels.reshape(img.shape[0], img.shape[1])
        
        # Visualize results
        plt.figure(figsize=(10, 5))
        plt.subplot(121)
        plt.imshow(img)
        plt.title(f'Original Image {"A" if i==0 else "B"}')
        plt.axis('off')

        plt.subplot(122)
        plt.imshow(seg_img, cmap='jet')
        plt.title('Recursive n-cuts Segmentation')
        plt.axis('off')
        plt.savefig(f'demo3c_img{"A" if i==0 else "B"}.png')
        plt.show()
        
if __name__ == "__main__":
    main()