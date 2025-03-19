import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import logging
import pandas as pd  # For graph plotting

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load trained model
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model("final_waste_classification_model.h5")
        logging.info("✅ Model loaded successfully!")
        return model
    except Exception as e:
        logging.error(f"❌ Model loading failed: {e}")
        st.error("Model could not be loaded. Check logs.")
        return None

model = load_model()

# Define class labels and descriptions
waste_info = {
    "Dry Waste": {
        "description": "Dry waste includes paper, plastic, metal, glass, and cardboard. These should be recycled properly.",
        "bin": "Blue Bin (Recyclable Waste)",
        "bin_image": "assets/blue_bin.png"
    },
    "Wet Waste": {
        "description": "Wet waste includes food scraps, vegetable peels, and garden waste. It should be composted or disposed in a wet waste bin.",
        "bin": "Green Bin (Organic Waste)",
        "bin_image": "assets/green_bin.png"
    }
}

# Streamlit UI
st.title("♻️ WasteSort AI")
st.write("Upload an image and click the **Predict** button to classify.")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
predict_button = st.button("🔍 Predict")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if predict_button and model:
        try:
            # Convert to NumPy array and preprocess
            img = np.array(image)
            img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
            img = img / 255.0  # Normalize
            img = np.expand_dims(img, axis=0)

            # Predict
            prediction = model.predict(img)[0]  # Extract prediction array
            
            # Since the model is binary, use a threshold to determine class
            threshold = 0.5
            if prediction[0] > threshold:
                dry_confidence = prediction[0] * 100
                wet_confidence = 100 - dry_confidence
            else:
                wet_confidence = (1 - prediction[0]) * 100
                dry_confidence = 100 - wet_confidence

            # Determine final classification
            detected_class = "Dry Waste" if dry_confidence > wet_confidence else "Wet Waste"
            confidence = max(dry_confidence, wet_confidence)
            other_class = "Wet Waste" if detected_class == "Dry Waste" else "Dry Waste"
            other_confidence = 100 - confidence

            # Get waste info
            waste_details = waste_info.get(detected_class, {"description": "Unknown Waste", "bin": "Unknown", "bin_image": None})

            # Display result
            st.write(f"### Classification: **{detected_class}** ({confidence:.2f}%)")
            st.write(f"📌 **What to do?** {waste_details['description']}")
            st.write(f"🗑 **Dispose in:** {waste_details['bin']}")

            # Show recommended bin image
            if waste_details["bin_image"]:
                st.image(waste_details["bin_image"], caption=waste_details["bin"], use_container_width=True)

            # Properly format the graph data
            confidence_data = pd.DataFrame(
                {"Confidence (%)": [confidence, other_confidence]},
                index=[detected_class, other_class]
            )
            st.bar_chart(confidence_data)

            # Log prediction
            logging.info(f"✅ Prediction: {detected_class} ({confidence:.2f}%)")

        except Exception as e:
            logging.error(f"❌ Error processing image: {e}")
            st.error("Image processing failed. Check logs.")
