from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import eigs
from sklearn.cluster import KMeans
import numpy as np


def n_cuts(affinity_mat: np.ndarray, k: int) -> np.ndarray:
    """
    Performs image segmentation using the non-recursive Normalized Cuts method.
    """
    W_sparse = csr_matrix(affinity_mat)
    D = np.sum(affinity_mat, axis=1)
    D_sparse = diags(D)

    # Laplacian array: L = D - W
    L_sparse = D_sparse - W_sparse

    # Generalized eigenvalue problem: Lx = λDx
    # Solve for the k smallest eigenvectors (SM = smallest magnitude)
    vals, vecs = eigs(L_sparse, k=k, M=D_sparse, which='SM')
    vecs = np.real(vecs)

    #  Apply k-means clustering to eigenvectors 
    kmeans = KMeans(n_clusters=k, random_state=1)

    # Cluster labels for each node
    cluster_idx = kmeans.fit_predict(vecs)

    return cluster_idx


def n_cuts_recursive(
    affinity_mat: np.ndarray,
    T1: int,
    T2: float
) -> np.ndarray:
    """
    Performs recursive normalized cuts segmentation until termination criteria are met.
    """
    n = affinity_mat.shape[0]
    cluster_idx = np.full(n, -1)  # In the beginning enery node without label
    current_label = [0]  # List for referrentiality in the recursion

    # Internal recursive function for hierarchical bipartion
    def recursive_split(nodes):
        if len(nodes) <= T1:
            cluster_idx[nodes] = current_label[0]
            current_label[0] += 1
            return
    
        # Affinity submatrix for current nodes
        sub_affinity = affinity_mat[np.ix_(nodes, nodes)]

        # Bipartition with n_cuts
        sub_cluster = n_cuts(sub_affinity, k=2)

        # Subgraphs
        A = [nodes[i] for i in range(len(nodes)) if sub_cluster[i] == 0]
        B = [nodes[i] for i in range(len(nodes)) if sub_cluster[i] == 1]

        # If one of the resulting subgraphs is < T1 nodes, the splitting stops
        if len(A) < T1 or len(B) < T1:
            cluster_idx[nodes] = current_label[0]
            current_label[0] += 1
            return

        # Calculation of Ncut value
        sub_cluster_full = np.zeros(len(nodes))
        for i in range(len(nodes)):
            sub_cluster_full[i] = sub_cluster[i]
        ncut_val = calculate_n_cut_value(sub_affinity, sub_cluster_full)

        # If the Ncut value is > T2, the splitting stops
        if ncut_val > T2:
            cluster_idx[nodes] = current_label[0]
            current_label[0] += 1
            return

        # If both resulting subgraphs are large enough and the Ncut 
        # value is low (≤ T2), the splitting continues recursively
        recursive_split(A)
        recursive_split(B)

    # Start with all nodes
    all_nodes = list(range(n))
    recursive_split(all_nodes)

    return cluster_idx


def calculate_n_cut_value(affinity_mat: np.ndarray, cluster_idx: np.ndarray) -> float:
    """
    Computes the Normalized Cut (Ncut) value for a bipartition of a graph.
    """
    A = np.where(cluster_idx == 0)[0]
    B = np.where(cluster_idx == 1)[0]

    assoc_A_A = np.sum(affinity_mat[np.ix_(A, A)])
    assoc_B_B = np.sum(affinity_mat[np.ix_(B, B)])
    assoc_A_V = np.sum(affinity_mat[A, :])
    assoc_B_V = np.sum(affinity_mat[B, :])

    nassoc = (assoc_A_A / assoc_A_V) + (assoc_B_B / assoc_B_V)
    ncut_value = 2 - nassoc

    return float(ncut_value)