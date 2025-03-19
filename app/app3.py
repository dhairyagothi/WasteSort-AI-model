import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import logging
import pandas as pd  # For graph plotting
from vit_keras import vit

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load trained ViT model
@st.cache_resource
def load_vit_model():
    try:
        model = tf.keras.models.load_model("final_vit_waste_classification_model.h5", compile=False)
        logging.info("✅ ViT Model loaded successfully!")
        return model
    except Exception as e:
        logging.error(f"❌ ViT Model loading failed: {e}")
        st.error("ViT Model could not be loaded. Check logs.")
        return None

vit_model = load_vit_model()

# Define class labels and descriptions
class_labels = ["Dry Waste", "Wet Waste"]

# Streamlit UI
st.title("♻️ WasteSort AI")
st.write("Upload an image and click the **Predict** button to classify using ViT.")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
predict_button = st.button("🔍 Predict")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if predict_button and vit_model:
        try:
            # Convert to NumPy array and preprocess
            img = np.array(image)
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
            img = img / 255.0  # Normalize
            img = np.expand_dims(img, axis=0)

            # Predict
            prediction = vit_model.predict(img)[0]  # Extract prediction array

            if len(prediction) == 1:  # Binary classification case (Sigmoid output)
                wet_confidence = prediction[0] * 100
                dry_confidence = (1 - prediction[0]) * 100
            else:  # Multi-class classification case (Softmax output)
                wet_confidence = prediction[0] * 100
                dry_confidence = prediction[1] * 100

            # Swap logic to correct misclassification
            if wet_confidence > dry_confidence:
                detected_class = "Wet Waste"
                confidence = wet_confidence
            else:
                detected_class = "Dry Waste"
                confidence = dry_confidence

            confidence_data = pd.DataFrame(
                {"Confidence (%)": [dry_confidence, wet_confidence]},
                index=["Dry Waste", "Wet Waste"]
            )

            # Display result
            st.write(f"### Classification: **{detected_class}** ({confidence:.2f}%)")
            st.bar_chart(confidence_data)
            logging.info(f"✅ Prediction: {detected_class} ({confidence:.2f}%)")
        
        except Exception as e:
            logging.error(f"❌ Error processing image: {e}")
            st.error("Image processing failed. Check logs.")