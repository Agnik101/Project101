import os
import cv2
import numpy as np

# Threshold value
minValue = 70

# Image processing function
def func(path):    
    frame = cv2.imread(path)
    if frame is None:
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)
    th3 = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    ret, res = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return res

# Input and output paths
input_base = r"D:\python\NewPRJ\dataSet\trainingData"
output_base = "data2"

# Create output directories
os.makedirs(os.path.join(output_base, "train"), exist_ok=True)
os.makedirs(os.path.join(output_base, "test"), exist_ok=True)

total = 0
train_count = 0
test_count = 0

# Loop through each subfolder in trainingData/ (each class label)
for label in os.listdir(input_base):
    label_path = os.path.join(input_base, label)

    # Skip files, only process directories
    if not os.path.isdir(label_path):
        continue

    print(f"Processing label: {label}")

    # Output paths
    train_dir = os.path.join(output_base, "train", label)
    test_dir = os.path.join(output_base, "test", label)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Get image files in the subfolder
    images = [f for f in os.listdir(label_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"  ➤ Found {len(images)} images in {label}")

    num_train = int(0.75 * len(images))

    for i, file in enumerate(images):
        img_path = os.path.join(label_path, file)
        try:
            processed_img = func(img_path)
            if processed_img is None:
                print(f"  ⚠️ Warning: func() returned None for {img_path}")
                continue

            if i < num_train:
                save_path = os.path.join(train_dir, file)
                train_count += 1
            else:
                save_path = os.path.join(test_dir, file)
                test_count += 1

            cv2.imwrite(save_path, processed_img)
            total += 1
        except Exception as e:
            print(f"  ❌ Error processing {img_path}: {e}")

print(f"\n✅ Processing completed.")
print(f"🖼️ Total images processed: {total}")
print(f"📁 Train images: {train_count}")
print(f"📁 Test images: {test_count}")
