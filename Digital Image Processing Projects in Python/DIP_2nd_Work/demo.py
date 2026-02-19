import numpy as np
import matplotlib.pyplot as plt
from sobel_edge import sobel_edge
from log_edge import log_edge
from circ_hough import circ_hough
from PIL import Image

# Load the input image and convert to grayscale
# Normalize pixel values to the range [0, 1]
img = Image.open("basketball_large.png").convert("L")
img_arr = np.array(img).astype(float) / 255.0


# ------------------------------
# SOBEL EDGE DETECTION ANALYSIS
# ------------------------------
# Define different threshold values for Sobel edge detection
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5]
edge_counts = []

# Apply Sobel operator with different thresholds and display results
for th in thresholds:
    sobel_edges = sobel_edge(img_arr, th)
    edge_counts.append(np.sum(sobel_edges))

    # Display the binary edge map for each threshold
    plt.figure()
    plt.imshow(sobel_edges, cmap='gray')
    plt.title(f"Sobel Edge Map (Threshold = {th})")
    plt.axis('off')
    plt.show()

# Plot: Threshold vs Edge Pixel Count
plt.figure()
plt.plot(thresholds, edge_counts, marker='o')
plt.title("Number of Edge Pixels vs Threshold")
plt.xlabel("Threshold")
plt.ylabel("Edge Pixel Count")
plt.grid(True)
plt.show()


# ------------------------------
# LAPLACIAN OF GAUSSIAN DETECTION
# ------------------------------
# Apply LoG edge detection using pattern 3 (grid-based zero-crossing)
log_edges = log_edge(img_arr, 0.2, 3)  

# Display LoG result
plt.figure()
plt.imshow(log_edges, cmap='gray')
plt.title("LoG Edge Map")
plt.axis('off')
plt.show()


# ------------------------------
# HOUGH CIRCLE DETECTION
# ------------------------------
# Control flags to toggle between Sobel or LoG-based edge input
run_sobel = False
run_log = True

# Maximum expected radius for circles in image
R_max = 400

if run_sobel: # for sobel_edge
    # Use Sobel edge map as input for Hough transform
    binary_edge_map = sobel_edge(img_arr, 0.4)  

    # Resolution of parameter space (a, b, r)
    dim = np.array([200, 200, 125]) 
    # dim = np.array([1442, 1070, 10]) # With these values it needs approximately 10 minutes to run

    # Test different minimum vote thresholds
    vmins = [500, 750, 1000, 1250, 1600]
    # vmins = [20, 30, 40, 50, 60] 

if run_log: # for log_edge
    binary_edge_map = log_edge(img_arr, 0.2, 3)
    dim = np.array([200, 200, 125]) 
    vmins = [200, 300, 400, 500, 580]

# Detect circles for each V_min value and visualize results
for v in vmins:
    centers, radii = circ_hough(binary_edge_map, R_max, dim, V_min=v)

    # Plot original image with detected circles overlaid
    plt.figure()
    plt.imshow(img, cmap='gray')
    for (a, b), r in zip(centers, radii):
        circle = plt.Circle((b, a), r, color='red', fill=False, linewidth=1.5)
        plt.gca().add_patch(circle)

    plt.title(f"Hough Circles (V_min = {v})")
    plt.axis('off')
    plt.show()