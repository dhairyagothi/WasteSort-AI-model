import os
import shutil
import logging

# Enable logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Define dataset paths
DATASET_DIR = "dataset/RealWaste"
OUTPUT_DIR = "binary_dataset"

# Define dry and wet waste categories
DRY_WASTE_CATEGORIES = [
    "brown-glass", "cardboard", "clothes", "green-glass", "metal", 
    "paper", "plastic", "shoes", "white-glass","glass", "trash","metal","Glass" ,"Metal" ,"Miscellaneous Trash" ,"Plastic" ,"Paper" ,"Cardboard" ,"Clothes" ,"Shoes" ,"Trash" ,"Brown Glass" ,"Green Glass" ,"White Glass",
]
WET_WASTE_CATEGORIES = ["biological", "battery" ,"Food Organics" , "Vegetation"]

# Create output directories
dry_path = os.path.join(OUTPUT_DIR, "Dry Waste")
wet_path = os.path.join(OUTPUT_DIR, "Wet Waste")

os.makedirs(dry_path, exist_ok=True)
os.makedirs(wet_path, exist_ok=True)

# Function to copy images
def copy_images(source_folder, destination_folder):
    if not os.path.exists(source_folder):
        logging.warning(f"⚠️ Folder not found: {source_folder}")
        return
    
    for img_name in os.listdir(source_folder):
        src_path = os.path.join(source_folder, img_name)
        dest_path = os.path.join(destination_folder, img_name)
        
        # Ensure it's a valid file
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
            logging.info(f"✅ Copied {img_name} -> {destination_folder}")

# Organizing the dataset
logging.info("🚀 Starting dataset reorganization...")

for category in DRY_WASTE_CATEGORIES:
    copy_images(os.path.join(DATASET_DIR, category), dry_path)

for category in WET_WASTE_CATEGORIES:
    copy_images(os.path.join(DATASET_DIR, category), wet_path)

logging.info("🎉 Dataset reorganization completed!")
logging.info(f"📂 Dry Waste images stored in: {dry_path}")
logging.info(f"📂 Wet Waste images stored in: {wet_path}")
