import numpy as np
import cv2
import matplotlib.pyplot as plt

# -------------------------------
# Function: Compress image using SVD
# -------------------------------
def compress_image(channel, k):
    # Perform SVD
    U, S, Vt = np.linalg.svd(channel, full_matrices=False)

    # Keep only top k singular values
    S_k = np.diag(S[:k])
    U_k = U[:, :k]
    Vt_k = Vt[:k, :]

    # Reconstruct compressed image
    compressed = np.dot(U_k, np.dot(S_k, Vt_k))

    return compressed

# -------------------------------
# Load Image
# -------------------------------
img = cv2.imread("image_for_laa.jpeg")

if img is None:
    print("Error: Image not found!")
    exit()

# Convert to RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Normalize (0 to 1 for better SVD stability)
img = img / 255.0

# Split channels
R = img[:, :, 0]
G = img[:, :, 1]
B = img[:, :, 2]

# -------------------------------
# Choose k values (compression levels)
# -------------------------------
k_values = [5, 20, 50, 100]

compressed_images = []

for k in k_values:
    R_c = compress_image(R, k)
    G_c = compress_image(G, k)
    B_c = compress_image(B, k)

    compressed = np.stack((R_c, G_c, B_c), axis=2)

    # Clip values to valid range
    compressed = np.clip(compressed, 0, 1)

    compressed_images.append((k, compressed))

# -------------------------------
# Display Results
# -------------------------------
plt.figure(figsize=(12, 8))

# Original image
plt.subplot(2, 3, 1)
plt.imshow(img)
plt.title("Original")
plt.axis('off')

# Compressed images
for i, (k, comp_img) in enumerate(compressed_images):
    plt.subplot(2, 3, i + 2)
    plt.imshow(comp_img)
    plt.title(f"k = {k}")
    plt.axis('off')

plt.tight_layout()
plt.show()