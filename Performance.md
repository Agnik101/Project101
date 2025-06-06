# 📊 Model Performance Report

## ✅ Final Accuracy
- **Overall Accuracy:** 94%

---

## 🧪 Challenges Faced

### 🚧 During Training
1. **Dataset Collection**
   - Public datasets for sign language gestures were limited.
   - Had to supplement or fully create my own dataset by capturing images manually.

2. **Custom Dataset Preparation**
   - Each gesture image was captured under consistent lighting and background conditions.
   - Manual labeling was time-consuming but essential for accuracy.

3. **Directory Structure Setup**
   - Dataset was structured using a folder-per-class format:
     ```
     ├── data/
         ├── A/
         ├── B/
         ├── C/
         ...
     ```
   - Required for `ImageDataGenerator` and other loaders to work correctly in Keras.

---

### 🎯 During Prediction
1. **Camera Limitation**
   - Used the **laptop's built-in webcam**, which had limited resolution and frame rate.
   - No access to external high-quality cameras.

2. **Environmental Conditions**
   - Accurate predictions required:
     - **Proper lighting**
     - **Plain/noise-free background**
   - Inconsistent conditions led to lower prediction confidence and occasional misclassifications.

---

## 🚀 Future Improvements

### 🔄 Modular Model Architecture
- Propose integrating separate models trained for similar-looking gestures:
  - **TKDI model** for signs: T, K, D, I
  - **SMN model** for signs: S, M, N
  - **DRU model** for signs: D, R, U
- These models will specialize in distinguishing subtle hand differences and reduce misclassification.

### 🧠 Enhanced Model Complexity
- Use ensemble techniques to combine predictions from specialized models.
- Apply soft voting or majority consensus to increase final prediction accuracy up to **97%**.

### 🔧 Technical Enhancements
- **Use external HD camera** for better video feed.
- **Improve preprocessing pipeline**:
  - Background subtraction
  - Brightness normalization
  - Frame smoothing

### 📈 Data Augmentation
- Apply:
  - Rotation
  - Flip
  - Zoom
  - Brightness and contrast adjustments
- This will improve generalization and robustness.

---

## 📌 Conclusion
This project achieved a **94% accuracy**, demonstrating effective sign recognition under controlled conditions. With hardware upgrades and model modularization, this accuracy can be further improved to 97% or higher.

