from keras.models import load_model

# Load broken model with compile=False
model = load_model("model/emotion_model.h5", compile=False)

# Save new model without training config
model.save("model/emotion_model_cleaned.h5")
