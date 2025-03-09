import numpy as np
import cvxpy as cp
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
            with open(archive_name, "wb") as file:
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

    # indices_train = np.random.choice(len(x_train), train_size, replace=False)
    # indices_test = np.random.choice(len(x_test), test_size, replace=False)

    # return (
    #     x_train[indices_train],  # Training data
    #     y_train[indices_train],  # Training labels
    #     x_test[indices_test],    # Testing data
    #     y_test[indices_test]     # Testing labels
    # )
    return x_train, y_train, x_test, y_test

# Principal Component Analysis (PCA) for dimensionality reduction
def pca(X, n_components=0.91):
    X_mean = np.mean(X, axis=0)
    X_centered = X - X_mean  # Center the data

    # Compute covariance matrix and its eigenvalues/eigenvectors
    cov_matrix = np.cov(X_centered, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

    # Sort eigenvalues and eigenvectors in descending order
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # Determine number of components to retain
    total_variance = np.sum(eigenvalues)
    explained_variance = np.cumsum(eigenvalues) / total_variance
    num_components = np.argmax(explained_variance >= n_components) + 1

    print(f"Selected {num_components} components retaining {n_components*100}% variance.")

    # Project data onto lower-dimensional space
    selected_eigenvectors = eigenvectors[:, :num_components]
    reduced_X = np.dot(X_centered, selected_eigenvectors)

    return reduced_X, selected_eigenvectors, X_mean

# Kernel functions
def linear_kernel(x1, x2):
    return np.dot(x1, x2)

def polynomial_kernel(x1, x2, degree=2):
    return (np.dot(x1, x2) + 1) ** degree

def rbf_kernel(x1, x2, gamma=0.01):
    return np.exp(-gamma * np.linalg.norm(x1 - x2)**2)

# Support Vector Machine (SVM) implementation
class SVM:
    def __init__(self, kernel, C=10):
        self.kernel = kernel  # Kernel function
        self.C = C  # Regularization parameter

    def train(self, x_train, y_train):
        self.kernel_matrix = np.zeros((len(x_train), len(x_train)))
        self.x_train = x_train
        self.y_train = y_train

        # Compute the kernel matrix (Gram matrix)
        for i in range(len(x_train)):
            for j in range(len(x_train)):
                self.kernel_matrix[i, j] = y_train[i] * y_train[j] * self.kernel(x_train[i], x_train[j])
        self.kernel_matrix += np.eye(self.kernel_matrix.shape[0]) * 1e-10  # Regularization term

        # Solve quadratic optimization problem
        c = np.ones(len(x_train))
        self.a = cp.Variable(len(x_train))
        objective = cp.Minimize(0.5 * cp.quad_form(self.a, self.kernel_matrix) - c.T @ self.a)
        constraints = [self.a >= 0, self.a <= self.C]
        problem = cp.Problem(objective, constraints)
        problem.solve()  # Lagrange multipliers
        self.a = self.a.value

        # Identify support vectors
        epsilon = 1e-6
        svi = np.where((self.a > epsilon) & (self.a < self.C - epsilon))[0]
        print("Total support vectors:", len(svi))

        # Compute bias term
        if len(svi) > 0:
            self.b = 0;
            biases = []
            for sv in svi:
                b_sv = y_train[sv]
                for i in range(len(x_train)):
                    b_sv -= self.a[i] * y_train[i] * self.kernel(x_train[sv], x_train[i])
                biases.append(b_sv)
            self.b = np.mean(biases)
            print("Bias (b):", self.b)
        else:
            print("No support vectors found!")

    # Prediction function
    def predict(self, x):
        ker_matrix = np.zeros((len(x), len(self.x_train)))
        for i in range(len(x)):
            for j in range(len(self.x_train)):
                ker_matrix[i, j] = self.y_train[j] * self.kernel(x[i], self.x_train[j])

        predictions = np.dot(ker_matrix, self.a) + self.b
        return predictions

# Display examples of correct and incorrect classifications
def print_predictions_summary(test_labels, final_predictions, num_examples=5):
    correct_indices = np.where(final_predictions == test_labels)[0]
    incorrect_indices = np.where(final_predictions != test_labels)[0]

    print("\nCorrectly classified examples:")
    for i in range(min(num_examples, len(correct_indices))):
        index = correct_indices[i]
        print(f"Index: {index}, True label: {test_labels[index]}, Predicted label: {final_predictions[index]}")

    print("\nMisclassified examples:")
    for i in range(min(num_examples, len(incorrect_indices))):
        index = incorrect_indices[i]
        print(f"Index: {index}, True label: {test_labels[index]}, Predicted label: {final_predictions[index]}")

# Compute accuracy
def compute_accuracy(true_labels, predictions):
    return np.mean(true_labels == predictions) * 100

# Main program
def main():
    # Load dataset
    train_data, train_labels, test_data, test_labels = load_cifar10_data()
    print(f"Training samples: {train_data.shape[0]}, Test samples: {test_data.shape[0]}")

    # Apply PCA
    print("Applying PCA...")
    train_data_pca, selected_eigenvectors, train_data_mean = pca(train_data, 0.91)

    # Transform test data using the same PCA
    test_data_centered = test_data - train_data_mean
    test_data_pca = np.dot(test_data_centered, selected_eigenvectors)

    # Training SVM in batches
    batch_size = 1000
    batches_number = train_data.shape[0] // batch_size

    # Variables initialization
    predictions_for_each_label = np.zeros((10, test_size))
    batch_predictions_test = np.zeros((batches_number, test_size))
    predictions_for_each_label_train = np.zeros((10, batches_number * batch_size))
    batch_predictions_train = np.zeros(batches_number * batch_size)

    start_time = time.time()
    for label in range(10):
        print(f"Processing class {label}...")
        for batch in range(batches_number):
            print(f"Εκπαίδευση στο batch {batch + 1}/{batches_number}...")
            # Batch data selection
            batch_start = batch * batch_size
            batch_end = (batch + 1) * batch_size
            x_train_batch = train_data_pca[batch_start:batch_end]
            y_train_batch = np.where(train_labels[batch_start:batch_end] == label, 1, -1)

            #  # Train SVM on current batch
            svm = SVM(kernel=polynomial_kernel, C=0.1)
            svm.train(x_train_batch, y_train_batch)

            # Predict on test and training batch
            batch_predictions_test[batch, :] = svm.predict(test_data_pca)
            batch_predictions_train[(batch * batch_size):((batch + 1) * batch_size)] = svm.predict(x_train_batch)

        # Combine predictions from all the batches
        predictions_for_each_label[label, :] = np.mean(batch_predictions_test, axis=0)
        predictions_for_each_label_train[label, :] = batch_predictions_train
        print(f"Προβλέψεις για την κλάση {label}:\n", predictions_for_each_label[label])

    # Compute final predictions and accuracy
    final_predictions_test = np.argmax(predictions_for_each_label, axis=0)
    final_predictions_train = np.argmax(predictions_for_each_label_train, axis=0)
    testing_accuracy = compute_accuracy(test_labels, final_predictions_test)
    training_accuracy = compute_accuracy(train_labels, final_predictions_train)

    print("Final predictions:", final_predictions_test)
    print(f"Training accuracy: {training_accuracy:.2f}%")
    print(f"Testing Accuracy: {testing_accuracy:.2f}%")
    print(f"Training time: {time.time() - start_time:.2f} seconds")

    # Print classification examples
    print_predictions_summary(test_labels, final_predictions_test)

if __name__ == "__main__":
    main()
