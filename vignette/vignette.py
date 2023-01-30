import os
import cv2
import numpy as np

file = os.getenv('IN_FILE')

img = cv2.imread(file)
rows, cols = img.shape[:2]

# Generating vignette mask using Gussian kernels
kernel_x = cv2.getGaussianKernel(cols, cols * 0.3 )
kernel_y = cv2.getGaussianKernel(rows, rows * 0.3 )
kernel = kernel_y * kernel_x.T

mask = 255 * kernel / np.linalg.norm(kernel)
output = np.copy(img)

# Apply the mask
for i in range(3):
    output[:,:,i] = output[:,:,i] * ( mask * 3 )


cv2.imwrite(os.getenv('OUT_FILE'), output)