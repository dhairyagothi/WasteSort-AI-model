import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.preprocessing import image
import sys

model = tf.keras.models.load_model("model/waste_classifier.h5")

# Class labels
class_labels = ["Dry Waste", "Wet Waste"]

# Load and preprocess image
img_path = sys.argv[1]
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
prediction = model.predict(img_array)
result = class_labels[int(prediction[0][0] > 0.5)]
print(f"🏷 Classification: {result}")
