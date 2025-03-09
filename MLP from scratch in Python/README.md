# Multi-Layer Perceptron (MLP) from Scratch for CIFAR-10 Classification

---

## Table of contents
- [Project Overview](#Project-Overview)
- [Features](#Features)
- [Installation](#Installation)
- [Dataset: CIFAR-10](#Dataset:-CIFAR--10)
- [Model Architecture](#Model-Architecture)
- [Training Process](#Training-Process)
- [Results](#Results)
- [Key Findings](#Key-Findings)
- [Future Improvements](#Future-Improvements)
- [Contact](#contact)

---

## 📌 Project Overview
This project implements a **Multi-Layer Perceptron (MLP) from scratch in Python** without using deep learning libraries like TensorFlow or PyTorch. The MLP is trained using **backpropagation** on the **CIFAR-10 dataset**, a dataset of 60,000 color images classified into 10 categories. It is developed as part of the **Neural Networks - Deep Learning** 
course from the **Computer Science** department of AUTH in the 8th semester of my studies.

The goal is to:
- Develop an MLP **without pre-built deep learning frameworks**.
- Train it using **batch gradient descent** and **cross-entropy loss**.
- Evaluate **different hyperparameters** to optimize performance.
- Compare performance with **nearest neighbor classifiers**.

## 🚀 Features
- **Fully connected feedforward neural network**
- **ReLU** activation for hidden layers, **Softmax** for output
- **Backpropagation with gradient descent**
- **Batch training with adjustable learning rate decay**
- **One-hot encoding for labels**
- **Shuffling and normalizing the dataset**
- **Performance visualization with Matplotlib**
- **Comparison with Nearest Neighbor classifiers**

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/MLP-from-Scratch.git
   cd MLP-from-Scratch
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Run the MLP model:**
   ```bash
   python mlp.py

## 📊 Dataset: CIFAR-10
- **10 categories**: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck.
- **50,000 training samples**, **10,000 test samples**.
- Downloaded and extracted automatically by the script.

---

## 🔧 Model Architecture
| Layer | Type | Activation |
|--------|----------------|------------|
| Input Layer | 3072 neurons (32x32x3) | - |
| Hidden Layer 1 | 256 neurons | ReLU |
| Hidden Layer 2 | 128 neurons | ReLU |
| Output Layer | 10 neurons | Softmax |

- **Loss Function:** Cross-Entropy
- **Optimizer:** Batch Gradient Descent
- **Learning Rate:** Adaptive (with decay factor `lr_decay`)

---

## 🏋️ Training Process
1. **Download & Load CIFAR-10 dataset** automatically.
2. **Normalize pixel values** (rescale between 0 and 1).
3. **One-hot encode labels** for classification.
4. **Initialize weights** using He Initialization.
5. **Perform forward and backward propagation** to update weights.
6. **Monitor training loss, test loss, and accuracy** across epochs.
7. **Visualize the learning curve** (Loss per epoch).

---

## 📈 Results
- **Best test accuracy achieved:** ~54.7%
- **Optimal architecture:** `[3072, 256, 128, 10]`
- **Improvement with batch training and learning rate scheduling.**
- **Comparison with Nearest Neighbor classifiers showed superior performance.**

---

## 📌 Key Findings
✔ Using **ReLU activation** significantly improved performance over Sigmoid.  
✔ **He Initialization** helped avoid vanishing/exploding gradients.  
✔ **Batch Training** reduced noise in gradient updates.  
✔ **Dynamic learning rate** improved convergence.  
✔ **More hidden layers** improved accuracy but increased training time.

---

## 📜 References
- CIFAR-10 Dataset: [https://www.cs.toronto.edu/~kriz/cifar.html](https://www.cs.toronto.edu/~kriz/cifar.html)
- Project description: *NN_MLP(1st)_Project.pdf*
- Full report: *Report_MLPfromscratch.pdf*

---

## ✨ Future Improvements
- Implement **Convolutional Neural Networks (CNNs)**
- Use **Dropout and Batch Normalization** for regularization.
- Implement **Adam Optimizer** for adaptive learning rates.

---

## Contact
* Name: Georgios Tsantikis
* Email: giotsa44@gmail.com
* GitHub: [geotsad](https://github.com/geotsad)

[Return to the top](#table-of-contents)
