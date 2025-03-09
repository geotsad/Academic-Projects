import numpy as np
import matplotlib.pyplot as plt
import pickle
import time
import requests
import tarfile
import os


# Download and extract the CIFAR-10 dataset
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

# Load dataset data
def load_cifar10():
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

    x_train = np.vstack(x).astype(np.float32) / 255.0  # Normalize values
    y_train = np.array(y)

    test_batch = unpickle(os.path.join(data_path, "test_batch"))
    x_test = test_batch[b'data'].astype(np.float32) / 255.0
    y_test = np.array(test_batch[b'labels'])

    return x_train, y_train, x_test, y_test


class MLP:
    def __init__(self, layer_sizes, learning_rate, batch_size):
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate  
        self.weights = []
        self.biases = []
        self.batch_size = batch_size  # Number of samples per batch

        # Initialize weights and biases for each layer
        for i in range(len(layer_sizes) - 1):
            stddev = np.sqrt(2 / layer_sizes[i])  # He Normal Initialization
            self.weights.append(np.random.randn(layer_sizes[i], layer_sizes[i + 1]) * stddev)
            self.biases.append(np.zeros((1, layer_sizes[i + 1])))

    def relu(self, u):
        return np.maximum(0, u)

    def relu_derivative(self, u):
        return (u > 0).astype(float)

    def softmax(self, u):
        exp_u = np.exp(u - np.max(u, axis=1, keepdims=True))  # Prevent overflow
        return exp_u / np.sum(exp_u, axis=1, keepdims=True)

    def forward_pass(self, x):
        self.outputs = [x]  # Activation function outputs (x is the input)
        self.u_values = []  # Values before activation function

        for i in range(len(self.weights)):
            u = np.dot(self.outputs[-1], self.weights[i]) + self.biases[i]
            self.u_values.append(u)  # Store u values
            if i == len(self.weights) - 1:
                output = self.softmax(u)
            else:
                output = self.relu(u)
            self.outputs.append(output)
        return self.outputs[-1]

    def backward_pass(self, y_true):  # Backpropagation
        m = y_true.shape[0]  # Adjust to actual batch size
        deltas = [self.outputs[-1] - y_true]  # Error at output layer

        for i in range(len(self.weights) - 2, -1, -1):
            delta = np.dot(deltas[0], self.weights[i + 1].T) * self.relu_derivative(self.u_values[i])
            deltas.insert(0, delta)  # Store errors from output to input layer

        for i in range(len(self.weights)):
            dw = np.dot(self.outputs[i].T, deltas[i]) / m
            db = np.sum(deltas[i], axis=0, keepdims=True) / m
            self.weights[i] -= self.learning_rate * dw
            self.biases[i] -= self.learning_rate * db

    def predict(self, x):
        predictions = self.forward_pass(x)
        return np.argmax(predictions, axis=1)

    def train(self, x_train, y_train, x_test, y_test, epochs, batch_size, initial_lr, wait, lr_decay):
        self.train_loss_history = []  # Store training loss history
        self.test_loss_history = []  # Store test loss history
        self.learning_rate = initial_lr  # Initial learning rate
        num_samples = x_train.shape[0]  # Total training samples
        best_loss = float('inf')  # Initially set best loss to infinity
        no_improvement_epochs = 0  # Counter for epochs without improvement
        y_test_onehot = one_hot_encode(y_test, 10)  # One-hot encoding for y_test

        for epoch in range(epochs):
            # Shuffle training data
            indices = np.arange(num_samples)  # Create index array
            np.random.shuffle(indices)  # Random shuffling
            x_train = x_train[indices]
            y_train = y_train[indices]

            # Initialize average loss and accuracy for each epoch
            epoch_train_loss, epoch_train_accuracy = 0, 0
            epoch_test_loss, epoch_test_accuracy = 0, 0
            num_batches = 0  # Number of batches

            for i in range(0, num_samples, batch_size):
                x_batch = x_train[i:i + batch_size]  # Input batch
                y_batch = y_train[i:i + batch_size]  # Label batch

                # Compute training loss and accuracy for the batch
                train_loss = -np.mean(np.sum(y_batch * np.log(self.forward_pass(x_batch) + 1e-8), axis=1))
                epoch_train_loss += train_loss

                train_pred = self.predict(x_batch)
                train_labels = np.argmax(y_batch, axis=1)
                train_accuracy = np.mean(train_pred == train_labels)
                epoch_train_accuracy += train_accuracy

                # Backpropagation for the batch
                self.backward_pass(y_batch)
                num_batches += 1

            # Compute total training loss and accuracy for the epoch
            epoch_train_loss /= num_batches
            epoch_train_accuracy /= num_batches

            # Compute test loss and accuracy for the epoch
            epoch_test_loss = -np.mean(np.sum(y_test_onehot * np.log(self.forward_pass(x_test) + 1e-8), axis=1))

            test_pred = self.predict(x_test)
            test_accuracy = np.mean(test_pred == y_test)

            self.train_loss_history.append(epoch_train_loss)
            self.test_loss_history.append(epoch_test_loss)

            # Update best loss if training loss improves
            if epoch_train_loss < best_loss:
                best_loss = epoch_train_loss
                no_improvement_epochs = 0
            else:
                no_improvement_epochs += 1
                # Reduce learning rate if no improvement for "wait" epochs
                if no_improvement_epochs >= wait and self.learning_rate > 1e-6:
                    self.learning_rate *= lr_decay
                    no_improvement_epochs = 0  # Reset counter

            # Print statistics
            print(f"Epoch {epoch+1}, Train loss: {epoch_train_loss:.4f}, Test Loss: {epoch_test_loss:.4f},"
                  f" Learning Rate: {self.learning_rate:.6f},"
                  f" Train Acc: {epoch_train_accuracy * 100:.2f}%, Test Acc: {test_accuracy * 100:.2f}%")


# Convert labels to one-hot encoding
def one_hot_encode(labels, num_classes):
    return np.eye(num_classes)[labels]  # Identity matrix creation

# Examples of correct and incorrect classifications
def display_examples(y_true, y_pred, num_examples):
    print("\nCorrect Classifications:")
    correct_indices = np.where(y_true == y_pred)[0]
    for i in correct_indices[:num_examples]:  # Up to num_examples
        print(f"Example {i}:")
        print(f"True Label (One-hot): {one_hot_encode([y_true[i]], 10)[0]}")
        print(f"Prediction (One-hot): {one_hot_encode([y_pred[i]], 10)[0]}")
        print("-" * 30)

    print("\nIncorrect Classifications:")
    incorrect_indices = np.where(y_true != y_pred)[0]
    for i in incorrect_indices[:num_examples]:
        print(f"Example {i}:")
        print(f"True Label (One-hot): {one_hot_encode([y_true[i]], 10)[0]}")
        print(f"Prediction (One-hot): {one_hot_encode([y_pred[i]], 10)[0]}")
        print("-" * 30)

# Main program
def main():
    # Load all dataset data
    x_train, y_train, x_test, y_test = load_cifar10()
    print(f"Loaded {len(x_train)} training samples and {len(x_test)} test samples")

    # One-hot encoding
    y_train_onehot = one_hot_encode(y_train, 10)
    y_test_onehot = one_hot_encode(y_test, 10)

    # Define network hyperparameters
    input_size = x_train.shape[1]  # 3072 features
    hidden_sizes = [256, 128]  # Two hidden layers with 256 and 128 neurons
    output_size = 10  # Number of categories
    initial_lr = 0.01  # Initial learning rate
    epochs = 250
    batch_size = 128
    wait = 2  # Number of epochs without improvement before reducing lr
    lr_decay = 0.7  # Learning rate reduction factor

    # Create and train the MLP
    layer_sizes = [input_size] + hidden_sizes + [output_size]
    model = MLP(layer_sizes, initial_lr, batch_size)
    start_time = time.time()
    model.train(x_train, y_train_onehot, x_test, y_test, epochs, batch_size, initial_lr, wait, lr_decay)
    training_time = time.time() - start_time
    print(f"Training time: {training_time:.2f} seconds")

    # Plot Training and Test Loss
    plt.plot(range(epochs), model.train_loss_history, label="Training Loss", color="blue")
    plt.plot(range(epochs), model.test_loss_history, label="Test Loss", color="red")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title("Loss per Epoch")
    plt.legend()
    plt.grid(True)
    plt.show()

    y_test_pred = model.predict(x_test)
    # Display examples of correct and incorrect classifications
    display_examples(y_test, y_test_pred, num_examples=3)

if __name__ == "__main__":
    main()
