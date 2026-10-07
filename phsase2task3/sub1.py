import numpy as np
import matplotlib.pyplot as plt
import cv2

def convolve(image, kernel):
    
    rows, cols = kernel.shape
    if rows % 2 == 0 or cols % 2 == 0:
        raise ValueError("Kernel must have odd dimensions.")
    
    kernel = np.flipud(np.fliplr(kernel))

    img_rows, img_cols = image.shape

    pad_height = rows // 2
    pad_width = cols // 2
    padded_image = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width)),
                          mode='constant', constant_values=0)
    
    output = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded_image[i:i + rows, j:j + cols]
            output[i, j] = np.sum(region * kernel)

    output = np.clip(output, 0, 255)
    return output.astype(np.uint8)

try:
    img = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("Image not found or cannot be read.")
except Exception as e:
    print(e)
    exit()

fig, axes = plt.subplots(2, 3, figsize=(12, 8))

axes[0, 0].imshow(img, cmap='gray')
axes[0, 0].set_title('Original Image')
axes[0, 0].axis('off')

axes[0, 1].imshow(convolve(img, np.ones((5, 5)) / 25), cmap='gray')
axes[0, 1].set_title('Box Filter')
axes[0, 1].axis('off')

axes[0, 2].imshow(convolve(img, np.array([[-1, 0, 1],
                                          [-2, 0, 2],
                                          [-1, 0, 1]])), cmap='gray')
axes[0, 2].set_title('Horizontal Sobel Filter')
axes[0, 2].axis('off')

axes[1, 0].imshow(convolve(img, np.array([[-1, -2, -1],
                                          [ 0,  0,  0],
                                          [ 1,  2,  1]])), cmap='gray')
axes[1, 0].set_title('Vertical Sobel Filter')
axes[1, 0].axis('off')

axes[1, 1].imshow(convolve(img, (1/16) * np.array([[1, 2, 1],
                                                   [2, 4, 2],
                                                   [1, 2, 1]])), cmap='gray')
axes[1, 1].set_title('Gaussian Blur')
axes[1, 1].axis('off')

size = 5
pad = size // 2
padded = np.pad(img, pad, mode='constant', constant_values=0)
median_output = np.zeros_like(img)

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        region = padded[i:i+size, j:j+size].astype(np.float32)
        median_output[i, j] = np.median(region)
axes[1, 2].imshow(median_output, cmap='gray')
axes[1, 2].set_title('Median Filter')
axes[1, 2].axis('off')

plt.tight_layout()
plt.show()
