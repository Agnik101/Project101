import cv2
import mediapipe as mp
import os
from tqdm import tqdm

def process_images(input_dir, output_dir, hands):
    for root, _, files in os.walk(input_dir):
        rel_path = os.path.relpath(root, input_dir)
        output_subdir = os.path.join(output_dir, rel_path)
        os.makedirs(output_subdir, exist_ok=True)

        for file in tqdm(files, desc=f"Processing {rel_path}"):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_subdir, file)

                if os.path.exists(output_path):
                    continue  # Skip already processed

                image = cv2.imread(input_path)
                if image is None:
                    print(f"Warning: Skipping unreadable file {input_path}")
                    continue

                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp.solutions.drawing_utils.draw_landmarks(
                            image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                cv2.imwrite(output_path, image)

if __name__ == "__main__":
    input_train_dir = r"D:\python\NewPRJ\dataSet\trainingData"
    input_test_dir = r"D:\python\NewPRJ\dataSet\testingData"
    output_base_dir = r"D:\python\NewPRJ\data2"

    mp_hands = mp.solutions.hands
    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.7) as hands:
        print("Processing training data...")
        process_images(input_train_dir, output_base_dir, hands)

        print("Processing testing data...")
        process_images(input_test_dir, output_base_dir, hands)

    print("Processing completed successfully.")
