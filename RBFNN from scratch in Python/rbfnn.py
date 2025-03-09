import numpy as np
import time
import pickle
import requests
import tarfile
import os

# Download and extract CIFAR-10 dataset
def download_and_extract_cifar10():
    url = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
    archive_name = "cifar-10-python.tar.gz"
    if not os.path.exists(archive_name):
        print("Downloading CIFAR-10 dataset...")
        with requests.get(url, stream=True) as r:
            with open(archive_name, "wb") as file:  # Open for writing
                file.write(r.content)
    if not os.path.exists("cifar-10-batches-py"):
        print("Extracting dataset...")
        with tarfile.open(archive_name, "r:gz") as tar:
            tar.extractall()

# Load CIFAR-10 dataset
def load_cifar10_data():
    def unpickle(file):
        with open(file, 'rb') as fo:
            data = pickle.load(fo, encoding='bytes')
        return data

    download_and_extract_cifar10()
    data_path = "./cifar-10-batches-py/"
    x, y = [], []

    for i in range(1, 6):
        batch = unpickle(os.path.join(data_path, f"data_batch_{i}"))
        x.append(batch[b'data'])
        y.extend(batch[b'labels'])

    x_train = np.vstack(x).astype(np.float32) / 255.0  # Normalize pixel values
    y_train = np.array(y)

    test_batch = unpickle(os.path.join(data_path, "test_batch"))
    x_test = test_batch[b'data'].astype(np.float32) / 255.0
    y_test = np.array(test_batch[b'labels'])

    return x_train, y_train, x_test, y_test

# PCA implementation
def pca(X, n_components=0.91):
    X_mean = np.mean(X, axis=0)
    X_centered = X - X_mean  # Centering data

    # Compute covariance matrix, eigenvalues, and eigenvectors
    cov_matrix = np.cov(X_centered, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

    # Sort eigenvalues in descending order
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # Compute total variance and select principal components
    total_variance = np.sum(eigenvalues)
    explained_variance = np.cumsum(eigenvalues) / total_variance
    num_components = np.argmax(explained_variance >= n_components) + 1

    print(f"Selected {num_components} components retaining {n_components*100}% variance.")

    # Project data onto lower-dimensional space
    selected_eigenvectors = eigenvectors[:, :num_components]
    reduced_X = np.dot(X_centered, selected_eigenvectors)

    return reduced_X, selected_eigenvectors, X_mean

# Least Squares method with regularization
def least_squares_with_regularization(G, Y, lambda_reg=1e-4):
    I = np.eye(G.shape[1])
    I[-1, -1] = 0  # Exclude bias term from regularization
    W = np.dot(np.linalg.inv(np.dot(G.T, G) + lambda_reg * I), np.dot(G.T, Y))
    return W

# K-Means clustering for selecting centers
def kmeans(X, n_clusters, random_state=None, max_iters=100):
    if random_state:
        np.random.seed(random_state)
    centers = X[np.random.choice(X.shape[0], n_clusters, replace=False)]
    for _ in range(max_iters):
        distances = np.linalg.norm(X[:, None] - centers[None, :], axis=2)
        labels = np.argmin(distances, axis=1)
        new_centers = np.array([X[labels == k].mean(axis=0) for k in range(n_clusters)])
        if np.all(centers == new_centers):
            break
        centers = new_centers
    return centers, labels

# Random center selection
def random_centers(X, n_clusters, random_state=None):
    if random_state:
        np.random.seed(random_state)
    indices = np.random.choice(X.shape[0], n_clusters, replace=False)
    centers = X[indices]
    return centers

# RBF layer activations
def rbf_activation(X, centers, betas):
    G = np.zeros((X.shape[0], centers.shape[0]))
    for i, center in enumerate(centers):
        distances = np.linalg.norm(X - center, axis=1)
        G[:, i] = np.exp(-betas[i] * distances ** 2)
    return G

# One-hot encoding function
def one_hot_encode(labels, num_classes):
    return np.eye(num_classes)[labels]  # Identity matrix

# Output layer activation function (Softmax)
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# Loss function (Cross-Entropy)
def cross_entropy_loss(Y_true, Y_pred):
    return -np.sum(Y_true * np.log(Y_pred + 1e-9)) / Y_true.shape[0]

# Compute accuracy
def compute_accuracy(true_labels, predictions):
    return np.mean(true_labels == predictions) * 100

# Display examples of correct and incorrect classifications
def display_examples(y_true, y_pred, num_examples):
    print("\nCorrectly Classified Examples:")
    correct_indices = np.where(y_true == y_pred)[0]
    for i in correct_indices[:num_examples]:  # Up to num_examples
        print(f"Example {i}:")
        print(f"True Label (One-hot): {one_hot_encode([y_true[i]], 10)[0]}")
        print(f"Predicted (One-hot): {one_hot_encode([y_pred[i]], 10)[0]}")
        print("-" * 30)

    print("\nMisclassified Examples:")
    incorrect_indices = np.where(y_true != y_pred)[0]
    for i in incorrect_indices[:num_examples]:
        print(f"Example {i}:")
        print(f"True Label (One-hot): {one_hot_encode([y_true[i]], 10)[0]}")
        print(f"Predicted (One-hot): {one_hot_encode([y_pred[i]], 10)[0]}")
        print("-" * 30)

# ==========================================
#            Back Propagation 
# ==========================================
"""
The following section of code contains the implementation of backpropagation
for training the output layer of the RBF network using gradient descent.
This section is currently commented out for clarity.
"""
'''
# Main function
def main():
    X_train, Y_train, X_test, Y_test = load_cifar10_data()

    print("Applying PCA to training data...")
    X_train_pca, selected_eigenvectors, X_train_mean = pca(X_train, 0.91)

    # Transform test set using the same PCA
    X_test_centered = X_test - X_train_mean
    X_test_pca = np.dot(X_test_centered, selected_eigenvectors)

    # Train the hidden RBF layer
    start_time = time.time()
    n_rbf_neurons = 100  # Number of hidden neurons/centers
    print("Applying k-means for center selection...")
    centers, _ = kmeans(X_train_pca, n_rbf_neurons, random_state=0)

    # Compute sigma and betas
    max_distance = np.max([np.linalg.norm(c1 - c2) for i, c1 in enumerate(centers) for j, c2 in enumerate(centers) if i != j])
    sigma = max_distance / np.sqrt(2 * n_rbf_neurons)
    betas = np.full(n_rbf_neurons, 1 / (2 * sigma ** 2))

    print("Sigma value:")
    print(sigma)

    # Compute RBF activations
    G_train = rbf_activation(X_train_pca, centers, betas)
    G_test = rbf_activation(X_test_pca, centers, betas)

    # Print statistics before normalization
    print(f"G_train before normalization: min={np.min(G_train)}, max={np.max(G_train)}, mean={np.mean(G_train)}")
    print(f"G_test before normalization: min={np.min(G_test)}, max={np.max(G_test)}, mean={np.mean(G_test)}")

    # Normalize G
    G_train /= np.max(G_train, axis=1, keepdims=True)
    G_test /= np.max(G_test, axis=1, keepdims=True)

    # Print statistics after normalization
    print(f"G_train after normalization: min={np.min(G_train)}, max={np.max(G_train)}, mean={np.mean(G_train)}")
    print(f"G_test after normalization: min={np.min(G_test)}, max={np.max(G_test)}, mean={np.mean(G_test)}")

    # Append bias term to G
    G_train_aug = np.hstack([G_train, np.ones((G_train.shape[0], 1))])
    G_test_aug = np.hstack([G_test, np.ones((G_test.shape[0], 1))])

    # One-hot encoding
    Y_train_one_hot = one_hot_encode(Y_train, 10)
    Y_test_one_hot = one_hot_encode(Y_test, 10)

    # Initialize hyperparameters and variables
    limit = np.sqrt(6 / (G_train_aug.shape[1] + 10))  # Xavier uniform
    weights = np.random.uniform(-limit, limit, size=(G_train_aug.shape[1], 10)) 
    learning_rate = 0.001 
    epochs = 100
    best_loss = float('inf')
    wait = 2
    no_improvement_epochs = 0
    lr_decay = 0.7
    num_examples = 3  # Number of examples to display

    # Train the output layer using Backpropagation
    for epoch in range(epochs):
        # Compute outputs
        train_outputs = np.dot(G_train_aug, weights)
        test_outputs = np.dot(G_test_aug, weights)

        # Convert outputs to probabilities (SoftMax)
        train_outputs_prob = softmax(train_outputs)
        test_outputs_prob = softmax(test_outputs)

        # Compute errors
        train_error = Y_train_one_hot - train_outputs_prob
        test_error = Y_test_one_hot - test_outputs_prob

        # Compute loss (Cross-Entropy)
        train_loss = cross_entropy_loss(Y_train_one_hot, train_outputs_prob) 
        test_loss = cross_entropy_loss(Y_test_one_hot, test_outputs_prob)

        # Update weights and bias
        weights += np.dot(G_train_aug.T, train_error) * learning_rate

        # Update best loss if improved
        if train_loss < best_loss:
            best_loss = train_loss
            no_improvement_epochs = 0
        else:
            no_improvement_epochs += 1
            # Reduce learning rate if no improvement for `wait` epochs
            if no_improvement_epochs >= wait and learning_rate > 1e-6:
                learning_rate *= lr_decay
                no_improvement_epochs = 0  # Reset counter
                print(f"Epoch {epoch + 1}/{epochs}: Reducing learning rate to {learning_rate:.6f}")

        # Compute predictions and accuracy
        train_predictions = np.argmax(train_outputs_prob, axis=1)
        test_predictions = np.argmax(test_outputs_prob, axis=1)
        train_accuracy = compute_accuracy(Y_train, train_predictions)
        test_accuracy = compute_accuracy(Y_test, test_predictions)

        print(f"Epoch {epoch + 1}/{epochs}: Train Loss = {train_loss:.4f}, Test Loss = {test_loss:.4f}, "
              f"Train Accuracy = {train_accuracy:.4f}, Test Accuracy = {test_accuracy:.4f}")

    total_training_time = time.time() - start_time
    print(f"Total Training Time: {total_training_time:.2f} seconds")

    # Display examples of correct and incorrect classifications
    print("\nExamples of correct and incorrect classifications:")
    display_examples(Y_test, test_predictions, num_examples)

if __name__ == "__main__":
    main()
'''

# ==========================================
#             Least Squares 
# ==========================================
# Main function
def main():
    X_train, Y_train, X_test, Y_test = load_cifar10_data()

    print("Applying PCA to training data...")
    X_train_pca, selected_eigenvectors, X_train_mean = pca(X_train, 0.91)

    # Transform test set using the same PCA
    X_test_centered = X_test - X_train_mean
    X_test_pca = np.dot(X_test_centered, selected_eigenvectors)

    # Train hidden RBF layer
    start_time = time.time()
    n_rbf_neurons = 1000  # Number of hidden neurons/centers
    print("Selecting random centers...")
    centers = random_centers(X_train_pca, n_rbf_neurons, random_state=0)

    # Compute sigma values per center
    sigma_per_center = np.zeros(centers.shape[0])
    for i, c1 in enumerate(centers):
        distances = [np.linalg.norm(c1 - c2) for j, c2 in enumerate(centers) if i != j]
        sigma_per_center[i] = np.mean(distances)

    print("Sigma value for each center:")
    print(sigma_per_center)

    betas = 1 / (2 * sigma_per_center ** 2)
  
    # Compute RBF activations
    G_train = rbf_activation(X_train_pca, centers, betas)
    G_test = rbf_activation(X_test_pca, centers, betas)

    # Print statistics before normalization
    print(f"G_train : min={np.min(G_train)}, max={np.max(G_train)}, mean={np.mean(G_train)}")
    print(f"G_test : min={np.min(G_test)}, max={np.max(G_test)}, mean={np.mean(G_test)}")
  
    # Append bias term
    G_train_aug = np.hstack([G_train, np.ones((G_train.shape[0], 1))])
    G_test_aug = np.hstack([G_test, np.ones((G_test.shape[0], 1))])

    # One hot encoding
    Y_train_one_hot = one_hot_encode(Y_train, 10)
    Y_test_one_hot = one_hot_encode(Y_test, 10)
  
    # Train output layer using Least Squares
    W = least_squares_with_regularization(G_train_aug, one_hot_encode(Y_train, 10))

    # Compute predictions
    train_outputs = np.dot(G_train_aug, W)
    test_outputs = np.dot(G_test_aug, W)

    # Transform outputs into probabilities (SoftMax)
    train_outputs_prob = softmax(train_outputs)
    test_outputs_prob = softmax(test_outputs)

    # Compute Loss (Cross-Entropy)
    train_loss = cross_entropy_loss(Y_train_one_hot, train_outputs_prob) 
    test_loss = cross_entropy_loss(Y_test_one_hot, test_outputs_prob)

    # Compute predictions and accuracy
    train_predictions = np.argmax(train_outputs_prob, axis=1)
    test_predictions = np.argmax(test_outputs_prob, axis=1)
    train_accuracy = compute_accuracy(Y_train, train_predictions)
    test_accuracy = compute_accuracy(Y_test, test_predictions)

    # Results
    print(f"Train Loss = {train_loss:.4f}, Test Loss = {test_loss:.4f}")
    print(f"Train Accuracy = {train_accuracy:.4f}, Test Accuracy = {test_accuracy:.4f}")

    total_training_time = time.time() - start_time
    print(f"Total training time: {total_training_time:.2f} seconds")

    # Print classification examples
    display_examples(Y_test, test_predictions, num_examples = 3)

if __name__ == "__main__":
    main()
