
# 🧩 Project Workflow Pipeline

This section outlines the step-by-step **Sign Language to Text Converter** pipeline — from gesture capture to building sentences using real-time predictions and spell checking.

---

## 🔄 Workflow Pipeline Overview

```text
  📷
  Webcam Input (Live Feed)
     │
     ▼
  📦
  Region of Interest (ROI) Extraction
     │
     ▼
  🧼
  Image Preprocessing (Grayscale, Resize, Threshold)
     │
     ▼
  🧠
  CNN Model Prediction (Keras)
     │
     ▼
  🔤
  Predicted Alphabet
     │
     ▼
  🧱
  Word Formation (Character Accumulation)
     │
     ▼
  🪄
  Spell Checker Suggestion (PySpeller)
     │
     ▼
  🧩
  Sentence Formation (Word Accumulation)
     │
     ▼
  🖥️
  Tkinter GUI Output
