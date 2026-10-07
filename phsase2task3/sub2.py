import numpy as np
import matplotlib.pyplot as plt
import cv2

img = cv2.imread('shapes.jpg')
if img is None:
    raise FileNotFoundError("Image 'shapes.jpg' not found")
img = img[:, :, ::-1]  
out = img.copy()

red  = (img[:, :, 0] > 200) & (img[:, :, 1] < 100) & (img[:, :, 2] < 100)
blue  = (img[:, :, 0] < 100) & (img[:, :, 1] < 100) & (img[:, :, 2] > 200)
black = (img[:, :, 0] < 50) & (img[:, :, 1] < 50) & (img[:, :, 2] < 50)

out[blue]  = (0, 0, 0)
out[red]   = (0, 0, 255)
out[black] = (255, 0, 0)

fig, axes = plt.subplots(1, 2)
axes[0].imshow(img)
axes[0].set_title('Original Image')
axes[0].axis('off')

axes[1].imshow(out)
axes[1].set_title('Processed Image')
axes[1].axis('off')

plt.show()