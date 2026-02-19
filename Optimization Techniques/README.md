# Optimization Techniques Algorithms (MATLAB)

## Table of Contents
* [Project Overview](#project-overview)
* [Implemented Algorithms](#implemented-algorithms)
  * [Part 1: 1D Optimization (Single Variable)](#part-1-1d-optimization)
  * [Part 2: Unconstrained Optimization (Multi-variable)](#part-2-unconstrained-optimization)
  * [Part 3: Constrained Optimization](#part-3-constrained-optimization)
* [Final Project](#final-project)
* [Technologies Used](#technologies-used)
* [Installation & Usage](#installation--usage)

## Project Overview
This repository contains a collection of optimization algorithms implemented from scratch in **MATLAB**. The project was developed as part of the "Optimization Techniques" course at the Electrical and Computer Engineering (ECE) department of the Aristotle University of Thessaloniki (AUTH) during the 7th semester.

The main objective is to understand, implement, and evaluate various mathematical methods used to find the local or global minimum of objective functions, analyzing their convergence rate, stability, and computational cost.

## Implemented Algorithms

### Part 1: 1D Optimization (Single Variable)
Focuses on finding the minimum of a function $f(x)$ within a specific interval $[a, b]$ without using built-in optimization functions.
* **Bisection Method (with derivatives):** Uses the root of the first derivative $f'(x)=0$ to halve the search interval.
* **Golden Section Search:** Eliminates sub-intervals iteratively based on the golden ratio, requiring only function evaluations.
* **Fibonacci Search:** Similar to the Golden Section but uses Fibonacci numbers to determine the test points for interval reduction.
* **Dichotomous Search (Bisection without derivatives):** Uses a small constant $\epsilon$ to evaluate points near the midpoint.

### Part 2: Unconstrained Optimization (Multi-variable)
Focuses on minimizing $f(x, y)$ where the variables can take any real value. Evaluated convergence with constant and variable learning rates (step sizes).
* **Steepest Descent (Gradient Descent):** Moves along the negative gradient to find the minimum.
* **Newton's Method:** Uses the Hessian matrix (second derivatives) for faster, quadratic convergence.
* **Levenberg-Marquardt Method:** A hybrid approach that interpolates between the Gauss-Newton algorithm and the method of gradient descent to ensure stability when the Hessian is not positive definite.

### Part 3: Constrained Optimization
Focuses on minimizing an objective function subject to equality or inequality constraints.
* **Steepest Descent with Projection:** An extension of the standard Gradient Descent that projects the new calculated point back into the feasible region defined by the system's constraints.

## Final Project
The comprehensive final project synthesizes the above methods, typically applying them to more complex, highly non-linear objective functions (e.g., Rosenbrock function). It includes:
* Extensive performance visualization (Contour plots, 3D surface plots of the objective function).
* Plotting the convergence path of the algorithms towards the optimal solution.
* Comparative analysis of iterations, function evaluations, and execution time.

## Technologies Used
* **Language:** MATLAB
* **Key Features:** Matrix operations, symbolic math (for gradients/Hessians), and 2D/3D plotting functions (`surf`, `contour`, `plot3`).

## Installation & Usage
1. Clone the repository:
   ```bash
   git clone [https://github.com/geotsad/Academic-Projects.git](https://github.com/geotsad/Academic-Projects.git)

2. Open MATLAB and set the cloned folder (e.g., Optimization-Techniques) as your current directory.

3. Each assignment (Work1, Work2, Work3, Project) is organized in its respective folder.

4. Run the main scripts (e.g., main.m or report_script.m) within each folder to view the results and generated plots.
