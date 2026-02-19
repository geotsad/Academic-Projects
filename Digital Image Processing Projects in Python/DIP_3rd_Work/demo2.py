from scipy.io import loadmat
from image_to_graph import image_to_graph
from spectral_clustering import spectral_clustering
import matplotlib.pyplot as plt


# Load data
data = loadmat('dip_hw_3.mat')
img_a = data['d2a'] 
img_b = data['d2b']

def main():
    # Process each image
    for i, img in enumerate([img_a, img_b]):
        # Construct affinity graph from image
        affinity = image_to_graph(img)
        
        # Execute clustering for k=2,3,4 (# clusters)
        for k in [2, 3, 4]:
            labels = spectral_clustering(affinity, k)
            seg_img = labels.reshape(img.shape[0], img.shape[1])
            
            # Visualize results
            plt.figure(figsize=(10, 5))
            plt.subplot(121)
            plt.imshow(img)
            plt.title(f'Original Image {"A" if i==0 else "B"}')
            plt.axis('off')

            plt.subplot(122)
            plt.imshow(seg_img, cmap='jet')
            plt.title(f'Segmentation (k={k})')
            plt.axis('off')
            plt.savefig(f'demo2_img{"A" if i==0 else "B"}_k{k}.png')
            plt.show()

if __name__ == "__main__":
    main()