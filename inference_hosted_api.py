import sys
import requests
import cv2
import os
import json
from datetime import datetime

# Ensure correct usage
if len(sys.argv) != 3:
    print("❌ Usage: python3 inference_hosted_api.py <input_image> <output_image>")
    sys.exit(1)

# Get image paths from command-line arguments
input_image_path = sys.argv[1]
output_image_path = sys.argv[2]

# Define constants
API_URL = "https://detect.roboflow.com"
API_KEY = "122aOY67jDoRdfvlcYg6"
MODEL_ID = "mosquito_faa/1"

# Validate input image
if not os.path.exists(input_image_path):
    print(f"❌ Error: Input image not found at {input_image_path}")
    sys.exit(1)

# Initialize Inference Client
response = requests.post(
    f"{API_URL}/{MODEL_ID}?api_key={API_KEY}",
    files={"file": open(input_image_path, "rb")}
)

if response.status_code != 200:
    print(f"❌ Error: Failed to process image - {response.text}")
    sys.exit(1)

# Parse inference results
result = response.json()
predictions = result.get("predictions", [])
faa_count = len(predictions)
print(f"✅ Total FAA detected: {faa_count}")

# Load the input image
image = cv2.imread(input_image_path)
if image is None:
    print(f"❌ Error: Unable to read input image {input_image_path}")
    sys.exit(1)

# Overlay bounding boxes and FAA count
for pred in predictions:
    x, y, width, height = (
        int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
    )
    confidence = pred["confidence"]
    label = "FAA"
    
    x1, y1, x2, y2 = x - width // 2, y - height // 2, x + width // 2, y + height // 2
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    text = f"{label}: {confidence:.2f}"
    cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# Overlay FAA count
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
info_text = f"{timestamp} | FAA Count: {faa_count}"
cv2.putText(image, info_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Save the output image
cv2.imwrite(output_image_path, image)
print(f"✅ Inference result saved at {output_image_path}")
