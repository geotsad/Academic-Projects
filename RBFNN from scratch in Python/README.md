# Radial Basis Function Neural Network (RBFNN) from Scratch for CIFAR-10 Classification

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Dataset: CIFAR-10](#dataset)
- [Model Architecture](#model-architecture)
- [Training Process](#training-process)
- [Results](#results)
- [Key Findings](#key-findings)
- [References](#references)
- [Future Improvements](#future-improvements)
- [Contact](#contact)

---

## Project Overview
This project implements a **Radial Basis Function Neural Network (RBFNN) from scratch in Python** without using machine learning libraries such as Scikit-Learn or TensorFlow. 
The RBFNN is trained for multi-class classification on the **CIFAR-10 dataset**, a dataset containing 60,000 color images classified into 10 categories.
This project was developed as part of the **Neural Networks - Deep Learning** course from the **Computer Science** department of AUTH in the 7th semester of my studies.

The main objectives are:
- Develop an **RBFNN without pre-built machine learning frameworks**.
- Train and test the model using **both backpropagation (BP) and least squares (LS)**.
- Use **Principal Component Analysis (PCA)** for dimensionality reduction.
- Evaluate and compare **different center selection methods** (K-Means, Random Selection).
- Compare the RBFNN performance with **Nearest Neighbor classifiers (1-NN, 3-NN, NCC)**.


---

## Features
- **Radial Basis Function (RBF) neural network implementation from scratch**.
- **Two training approaches**: Backpropagation & Least Squares.
- **Center selection methods**: K-Means clustering & Random Selection.
- **Gaussian RBF kernel for hidden layer activation**.
- **Softmax activation & Cross-Entropy Loss for classification**.
- **PCA for feature reduction before classification**.
- **Comparison with Nearest Neighbor classifiers (1-NN, 3-NN, NCC)**.
- **Performance visualization with Matplotlib**.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/geotsad/RBFNN-from-Scratch.git
   cd RBFNN-from-Scratch
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Run the MLP model:**
   ```bash
   python rbf.py

---

## Dataset: CIFAR-10
- **10 categories**: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck.
- **50,000 training samples**, **10,000 test samples**.
- Downloaded and extracted automatically by the script.

---

## Model Architecture
- **Input Layer**: 3072 neurons (32x32x3 pixels per image).
- **Hidden Layer**: RBF neurons (with centers selected via K-Means or Random Selection).
- **Activation Function**: Gaussian RBF.
- **Output Layer**: 10 neurons (one per class).
- **Output Activation**: Softmax.
- **Loss Function**: Cross-Entropy Loss.
- **Training Approaches**:
  - **Backpropagation** with gradient descent.
  - **Least Squares** method with regularization.

---

## Training Process
1. **Download & Load CIFAR-10 dataset** automatically.
2. **Normalize pixel values** (rescale between 0 and 1).
3. **Reduce dimensionality using PCA** (retain 91% variance).
4. **Select RBF centers using K-Means or Random Selection**.
5. **Compute activation values using Gaussian RBF function**.
6. **Train the output layer using**:
   - **Backpropagation with Cross-Entropy Loss**.
   - **Least Squares method with regularization**.
7. **Evaluate model performance on test data**.
8. **Compare RBFNN with Nearest Neighbor classifiers (1-NN, 3-NN, NCC)**.

---

## Results
- **Best test accuracy achieved:**
  - **Least Squares (Random centers):** ~53.1%  
  - **Backpropagation (K-Means centers):** ~35.6%  
- **PCA reduced computational complexity significantly** while preserving information.
- **K-Means selected centers improved classification a little compared to Random Centers, but it was much slower.**.
- **Backpropagation training was slower and achieved lower accuracy than Least Squares**.
- **Comparison with 1-NN, 3-NN, NCC showed that RBFNN performed better**.


---

## Key Findings
✔ **PCA improved efficiency without significant accuracy loss.**  
✔ **Least Squares training provided higher accuracy than Backpropagation.**  
✔ **K-Means selected centers improved classification a little compared to Random Centers, but it was much slower.**  
✔ **Gaussian RBF activation function captured complex data patterns well.**  
✔ **RBFNN performed better than Nearest Neighbor classifiers but required higher computational resources.**  

---

## References
- CIFAR-10 Dataset: [https://www.cs.toronto.edu/~kriz/cifar.html](https://www.cs.toronto.edu/~kriz/cifar.html)
- Project description: *NN_RBF(3rd)_Project.pdf*
- Full report: *Report_RBFfromscratch.pdf*
- RBF Theory: [https://en.wikipedia.org/wiki/Radial_basis_function_network](https://en.wikipedia.org/wiki/Radial_basis_function_network)

---

## Future Improvements
- Implement **adaptive sigma selection** for Gaussian RBF neurons.
- Use **Cross-Validation** for optimal hyperparameter selection.
- Experiment with **alternative center selection methods** (e.g., K-Medoids).
- Implement **different optimization techniques** (e.g., Adam, SGD).
- Extend the model to **larger datasets like ImageNet**.

---

## Contact
* Name: Georgios Tsantikis  
* Email: giotsa44@gmail.com  
* GitHub: [geotsad](https://github.com/geotsad)

[Return to the top](#table-of-contents)
