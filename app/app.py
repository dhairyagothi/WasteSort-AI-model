import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load trained model
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model("model/waste_classifier.h5")
        logging.info("✅ Model loaded successfully!")
        return model
    except Exception as e:
        logging.error(f"❌ Model loading failed: {e}")
        st.error("Model could not be loaded. Check logs.")
        return None

model = load_model()

# Define class labels
class_labels = ["Dry Waste", "Wet Waste", "Metal", "Plastic", "Glass", "Organic Waste", "Paper", "E-Waste", "Battery", "Clothes"]

# Streamlit UI
st.title("♻️ Waste Classification AI")
st.write("Upload an image and click the **Predict** button to classify.")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
predict_button = st.button("🔍 Predict")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if predict_button:
        try:
            # Convert to NumPy array and preprocess
            img = np.array(image)
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
            img = img / 255.0  # Normalize
            img = np.expand_dims(img, axis=0)

            # Predict
            prediction = model.predict(img)
            confidence = np.max(prediction) * 100
            predicted_class = class_labels[np.argmax(prediction)]

            # Display result
            st.write(f"### 🏷 Classification: **{predicted_class}** ({confidence:.2f}%)")
            logging.info(f"✅ Prediction: {predicted_class} ({confidence:.2f}%)")
            st.bar_chart(prediction.flatten())  # Show confidence levels for each class

        except Exception as e:
            logging.error(f"❌ Error processing image: {e}")
            st.error("Image processing failed. Check logs.")
