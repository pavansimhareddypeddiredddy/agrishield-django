# import json
# import tensorflow as tf
# from tensorflow.keras.models import model_from_json

# # Load config (architecture)
# with open("ai_logic/config.json", "r") as f:
#     model_config = json.load(f)

# # Rebuild model
# model = model_from_json(json.dumps(model_config))

# # Load weights
# model.load_weights("ai_logic/model.weights.h5")

# print("✅ Model + Weights Loaded Successfully")