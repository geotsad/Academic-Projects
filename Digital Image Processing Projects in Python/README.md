# Digital Image Processing Algorithms & Applications (Python)

## Table of Contents
* [Project Overview](#project-overview)
* [Implemented Algorithms](#implemented-algorithms)
  * [Assignment 1: Point and Histogram-Based Processing](#assignment-1-point-and-histogram-based-processing)
  * [Assignment 2: Filtering and Feature Extraction](#assignment-2-filtering-and-feature-extraction)
  * [Assignment 3: Graph-Based Image Segmentation](#assignment-3-graph-based-image-segmentation)
* [Technologies Used](#technologies-used)
* [Installation & Usage](#installation--usage)

## Project Overview
This repository contains a collection of Digital Image Processing and Computer Vision algorithms implemented from scratch in **Python**. It was developed as part of the "Digital Image Processing" course during the Spring Semester (2024-2025) at the Electrical and Computer Engineering (ECE) department of the Aristotle University of Thessaloniki (AUTH).

The objective of these projects is to explore fundamental image analysis techniques, ranging from basic spatial domain transformations and feature extraction to advanced, graph-based image segmentation methods.

## Implemented Algorithms

### Assignment 1: Point and Histogram-Based Processing
Focuses on enhancing image contrast and modifying pixel intensities without altering the spatial structure of the image.
* **Grayscale Transformations:** Implemented various point processing techniques to manipulate image brightness and contrast.
* **Histogram Equalization:** Enhanced the global contrast of images by effectively spreading out the most frequent intensity values.
* **Histogram Matching (Specification):** Transformed an image so that its histogram matches a specified target histogram.

### Assignment 2: Filtering and Feature Extraction
Explores spatial filtering techniques for extracting critical structural information from images.
* **Edge Detection:** Implemented **Sobel** and **Laplacian** operators to detect boundaries and sharp intensity transitions within images.
* **Shape Detection (Hough Transform):** Implemented the Hough Transform algorithm specifically designed for detecting circular objects in complex images.

### Assignment 3: Graph-Based Image Segmentation
Focuses on partitioning an image into multiple segments (sets of pixels) using advanced graph theory concepts to simplify its representation.
* **Graph Construction:** Modeled images as graphs where nodes represent pixels and edges represent the similarity (weights) between them.
* **Spectral Clustering:** Grouped pixels into clusters by analyzing the eigenvalues of the graph's Laplacian matrix.
* **Normalized Cuts (N-Cuts):** Implemented both recursive and non-recursive Normalized Cuts algorithms to segment images by minimizing the weights of edges connecting different segments while maximizing intra-segment similarity.

## Technologies Used
* **Language:** Python 3.x
* **Libraries:** * `NumPy` & `SciPy` (Mathematical operations and linear algebra)
  * `scikit-learn` (Clustering algorithms and machine learning utilities)
  * `Matplotlib` (Image visualization and plotting)
* **Environment:** Jupyter Notebook

## Installation & Usage
1. Clone the repository:
   ```bash
   git clone [https://github.com/geotsad/Academic-Projects.git](https://github.com/geotsad/Academic-Projects.git)

2. Navigate to the Digital-Image-Processing folder.
3. Install the required dependencies:
   ```bash
   pip install numpy scipy scikit-learn matplotlib jupyter
4. Launch Jupyter Notebook to view and run the code:
   ```bash
   jupyter notebook
