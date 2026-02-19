from scipy.io import loadmat
from spectral_clustering import spectral_clustering
import matplotlib.pyplot as plt


# Load data
data = loadmat('dip_hw_3.mat')
affinity_mat = data['d1a'] # Precomputed affinity matrix

def main():
    # Execute clustering for k=2,3,4 (# clusters)
    for k in [2, 3, 4]:
        labels = spectral_clustering(affinity_mat, k)
        
        # Visualize results
        plt.figure(figsize=(8, 4))
        plt.scatter(range(len(labels)), labels, c=labels, cmap='jet', s=5)
        plt.title(f'Spectral Clustering (k={k})')
        plt.xlabel('Node Index') # Pixel
        plt.ylabel('Cluster')
        plt.colorbar()
        plt.savefig(f'demo1_k{k}.png')
        plt.show()

if __name__ == "__main__":
    main()