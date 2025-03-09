# Support Vector Machine (SVM) from Scratch for CIFAR-10 Classification

---

## Table of contents
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
This project implements a **Support Vector Machine (SVM) from scratch in Python** without using pre-built machine learning libraries such as Scikit-Learn. 
The SVM is trained to classify **CIFAR-10 images** using various kernel functions and is developed as part of the **Neural Networks - Deep Learning** course 
from the **Computer Science** department of AUTH in the 8th semester of my studies.

The goal is to:
- Develop an **SVM classifier from scratch** without using high-level libraries.
- Train the SVM to classify **CIFAR-10** images.
- Evaluate different **kernel functions** (Linear, Polynomial, RBF) and hyperparameters.
- Reduce data dimensionality using **Principal Component Analysis (PCA)**.
- Compare **SVM performance with Nearest Neighbor classifiers (1-NN, 3-NN, NCC)** and **Multi-Layer Perceptron (MLP)**.

---

## Features
- **Support Vector Machine (SVM) implementation from scratch**
- **Three kernel functions**: Linear, Polynomial, Radial Basis Function (RBF)
- **Hinge Loss optimization** using **Convex Optimization (cvxpy)**
- **Batch training** to handle large-scale data efficiently
- **PCA (Principal Component Analysis)** for dimensionality reduction
- **Performance comparison with MLP and Nearest Neighbor classifiers**
- **Visualization of classification results and support vectors**

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/geotsad/SVM-from-Scratch.git
   cd SVM-from-Scratch
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Run the MLP model:**
   ```bash
   python svm.py

---

## Dataset: CIFAR-10
- **10 categories**: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck.
- **50,000 training samples**, **10,000 test samples**.
- Downloaded and extracted automatically by the script.

## Model Architecture
- **Support Vector Machine (SVM)**
- **Kernel functions**: Linear, Polynomial, RBF
- **Optimization Method**: Convex Optimization using Lagrange Multipliers
- **Dimensionality Reduction**: PCA (Retaining 91% of variance)

---

## Training Process
1. **Download & Load CIFAR-10 dataset** automatically.
2. **Normalize pixel values** (rescale between 0 and 1).
3. **Reduce dimensionality using PCA** (Retain 91% variance).
4. **Train SVM using different kernel functions**.
5. **Optimize Support Vectors using convex optimization (cvxpy)**.
6. **Evaluate classification performance** on test data.
7. **Compare SVM performance with Nearest Neighbor (1-NN, 3-NN, NCC) and MLP models**.

---

## Results
- **Best test accuracy achieved:**  
  - **Linear Kernel:** ~39.4%  
  - **Polynomial Kernel (degree 2):** ~47.1%  
  - **RBF Kernel (gamma=0.01):** ~52.1%

- **Batch training improved efficiency** while handling large datasets.
- **RBF Kernel achieved the highest test accuracy.**
- **Comparisons with 1-NN, 3-NN, NCC, and MLP were conducted.**

---

## Key Findings
✔ **RBF Kernel outperformed Linear and Polynomial kernel.**  
✔ **Batch Training was necessary due to computational complexity.**  
✔ **Higher-degree Polynomial Kernels led to overfitting.**  
✔ **PCA improved training efficiency while preserving classification performance.**  
✔ **SVM performed better than Nearest Neighbor classifiers but worse than MLP.**  

---

## References
- CIFAR-10 Dataset: [https://www.cs.toronto.edu/~kriz/cifar.html](https://www.cs.toronto.edu/~kriz/cifar.html)
- Project description: *NN_SVM(2nd)_Project.pdf*
- Full report: *Report_SVMfromscratch.pdf*
- SVM Theory: [https://en.wikipedia.org/wiki/Support_vector_machine](https://en.wikipedia.org/wiki/Support_vector_machine)

---

## Future Improvements
- Implement **Multi-Class SVM using One-vs-One strategy**.
- Experiment with **Stochastic Gradient Descent (SGD) for faster optimization**.
- Use **Cross-validation** for hyperparameter tuning.
- Extend to **larger datasets like ImageNet**.
- Compare performance with **Deep Learning models (CNNs, ResNet, etc.)**.

---

## Contact
* Name: Georgios Tsantikis  
* Email: giotsa44@gmail.com  
* GitHub: [geotsad](https://github.com/geotsad)

[Return to the top](#table-of-contents)
