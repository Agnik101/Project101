import os

def count_images_in_dir(directory):
    total = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                total += 1
    return total

train_dir = r'D:\python\NewPRJ\dataSet\trainingData'
test_dir = r'D:\python\NewPRJ\dataSet\testingData'

train_count = count_images_in_dir(train_dir)
test_count = count_images_in_dir(test_dir)

print(f"Total training images: {train_count}")
print(f"Total testing images: {test_count}")
print(f"Total dataset images: {train_count + test_count}")