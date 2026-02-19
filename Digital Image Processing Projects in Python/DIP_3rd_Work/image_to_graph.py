import numpy as np
from scipy.spatial.distance import cdist


def image_to_graph(img_array: np.ndarray) -> np.ndarray:
    """
    Converts an image into a fully-connected undirected graph using a Gaussian affinity function.
    """
    M, N, C = img_array.shape
    pixels = img_array.reshape(-1, C) # Flatten the image to a list of pixel vectors
    
    # Compute pairwise Euclidean distances between pixel feature vectors
    distances = cdist(pixels, pixels, metric='euclidean')
    
    # Construct the affinity matrix using Gaussian-like similarity
    affinity_mat = 1.0 / np.exp(distances)
    
    return affinity_mat