import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os

# Base path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ Load SavedModel
model_path = os.path.join(BASE_DIR, "ai_logic", "final_model")
model = tf.saved_model.load(model_path)

# Get inference function
infer = model.signatures["serving_default"]

# Load labels
labels_path = os.path.join(BASE_DIR, "ai_logic", "labels.txt")
with open(labels_path, "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# Load solutions
solutions_path = os.path.join(BASE_DIR, "ai_logic", "solutions.json")
with open(solutions_path, "r") as f:
    solutions = json.load(f)


def predict_disease(image_path):
    # ✅ Image preprocessing (VERY IMPORTANT)
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0).astype(np.float32)

    # 🔥 Run model
    predictions = infer(tf.constant(img))

    # ✅ Extract output safely
    output = list(predictions.values())[0].numpy()

    # ✅ Get prediction
    index = np.argmax(output)
    confidence = float(np.max(output)) * 100   # 🔥 FIXED (0–100)

    disease_name = class_names[index]

    return disease_name, confidence