# Digital Image Processing Algorithms & Applications (MATLAB)

## Table of Contents
* [Project Overview](#project-overview)
* [Implemented Algorithms](#implemented-algorithms)
  * [Assignment 1: Image Resampling & Quantization](#assignment-1-image-resampling--quantization)
  * [Assignment 2: Frequency Domain & Image Transforms](#assignment-2-frequency-domain--image-transforms)
  * [Assignment 3: [Fill in Topic]](#assignment-3-fill-in-topic)
* [Technologies Used](#technologies-used)
* [Installation & Usage](#installation--usage)

## Project Overview
This repository contains a collection of Digital Image Processing algorithms implemented in **MATLAB**. It was developed as part of the "Digital Image Processing" course during the 8th semester at the Electrical and Computer Engineering (ECE) department of the Aristotle University of Thessaloniki (AUTH).

The objective of these projects is to explore core image processing concepts, ranging from spatial domain manipulations (interpolation, quantization) to frequency domain transformations (DFT, DCT) and image compression techniques.

## Implemented Algorithms

### Assignment 1: Image Resampling & Quantization
Focuses on spatial domain operations, altering image resolution, and reducing the number of discrete gray levels.
* **Downsampling & Upsampling:** Altering image resolution by decimation and subsequent reconstruction.
* **Interpolation Methods:** Implemented **Nearest Neighbor** and **Bilinear** interpolation from scratch to resize images and compared their visual quality.
* **Image Quantization:** Reduced the grayscale levels of images (e.g., from 256 to 128, 64, ..., 2 levels) to observe the effects of false contouring.
* **Error Evaluation:** Calculated the Mean Squared Error (MSE) between the original and processed images to quantify degradation.

### Assignment 2: Frequency Domain & Image Transforms
Explores the mathematical transformations of images into the frequency domain and their practical applications in compression.
* **2D Discrete Fourier Transform (DFT):** Analyzed the magnitude and phase components of various images.
* **Phase vs. Magnitude Reconstruction:** Demonstrated the critical importance of phase in human visual perception by reconstructing images using the phase of one image and the magnitude of another.
* **2D Discrete Cosine Transform (DCT):** Applied the DCT for energy compaction.
* **Image Compression:** Performed lossy compression by retaining only a specific percentage of the most significant DCT coefficients and evaluated the resulting MSE.

### Assignment 3: [Fill in Topic, e.g., Spatial Filtering & Edge Detection]
* [Add bullet 1: Briefly explain what you did, e.g., Implemented Sobel/Prewitt edge detectors]
* [Add bullet 2: Briefly explain the goal, e.g., Applied Gaussian smoothing filters to remove salt-and-pepper noise]

## Technologies Used
* **Language:** MATLAB
* **Key Toolboxes:** Image Processing Toolbox

## Installation & Usage
1. Clone the repository:
   ```bash
   git clone [https://github.com/geotsad/Academic-Projects.git](https://github.com/geotsad/Academic-Projects.git)
