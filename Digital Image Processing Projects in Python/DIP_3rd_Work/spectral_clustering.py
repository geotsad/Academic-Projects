import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import eigs
from sklearn.cluster import KMeans


def spectral_clustering(affinity_mat: np.ndarray, k: int) -> np.ndarray:
    """
    Performs spectral clustering (k clusters) on a graph defined by an affinity matrix.
    """
    # Compute diagonal arary D (each element of D's diagonal is the sum of W row respectively)
    W_sparse = csr_matrix(affinity_mat)
    D = np.sum(affinity_mat, axis=1)
    D_sparse = diags(D)

    # Laplacian array L = D - W (sparse for efficiency)
    L_sparse = D_sparse - W_sparse
    
    # Solve for the k smallest eigenvectors (SM = smallest magnitude)
    _, eigvecs = eigs(L_sparse, k=k, which='SM')
    U = np.real(eigvecs) # the array with columns the k smallest eigenvectors

    #  Apply k-means clustering to eigenvectors (line by line)
    kmeans = KMeans(n_clusters=k, random_state=1)
    kmeans.fit(U)

    # Cluster labels for each node
    cluster_idx = kmeans.labels_.astype(float)

    return cluster_idx

    # # Compute diagonal arary D (sum of W rows)
    # W = affinity_mat
    # D = diags(np.sum(affinity_mat, axis=1))

    # # Laplacian array L = D - W
    # L = D - W
    
    # # Solve for the k smallest eigenvectors (SM = smallest magnitude)
    # _, eigvecs = eigs(L, k=k, which='SM')
    # U = np.real(eigvecs) # the array with columns the k smallest eigenvectors