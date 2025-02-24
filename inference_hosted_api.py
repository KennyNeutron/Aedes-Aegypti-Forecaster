from inference_sdk import InferenceHTTPClient
import cv2
import os
import json
from datetime import datetime

# Define constants
API_URL = "https://detect.roboflow.com"
API_KEY = "122aOY67jDoRdfvlcYg6"
MODEL_ID = "mosquito_faa/1"
IMAGE_PATH = "images/sample_0002.jpg"
OUTPUT_IMAGE_PATH = "images/output.jpg"

# Initialize Inference Client
CLIENT = InferenceHTTPClient(api_url=API_URL, api_key=API_KEY)


def run_inference(image_path):
    print(f"Running inference on {image_path}...")
    try:
        # Run inference using the hosted API
        result = CLIENT.infer(image_path, model_id=MODEL_ID)

        # Debug: Print raw API response
        print("Raw API Response:", json.dumps(result, indent=2))

        # Extract predictions
        predictions = result.get("predictions", [])
        faa_count = len(predictions)
        print(f"Total FAA detected: {faa_count}")

        # Visualize detections
        visualize_predictions(image_path, predictions)

    except Exception as e:
        print(f"Error running inference: {e}")


def visualize_predictions(image_path, predictions):
    if not predictions:
        print("No predictions to visualize.")
        return

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read image {image_path}")
        return

    for prediction in predictions:
        x = int(prediction["x"])
        y = int(prediction["y"])
        width = int(prediction["width"])
        height = int(prediction["height"])
        confidence = prediction["confidence"]
        label = "FAA"  # Replace label with "FAA"

        # Calculate bounding box coordinates
        x1 = x - width // 2
        y1 = y - height // 2
        x2 = x + width // 2
        y2 = y + height // 2

        # Draw the bounding box with a new color (Red) and thinner line
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 1)

        # Add label and confidence in red with a smaller font
        text = f"{label}: {confidence:.2f}"
        cv2.putText(
            image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1
        )

    # Save the output image
    cv2.imwrite(OUTPUT_IMAGE_PATH, image)
    print(f"Result saved to {OUTPUT_IMAGE_PATH}")


# Main workflow
if __name__ == "__main__":
    if os.path.exists(IMAGE_PATH):
        run_inference(IMAGE_PATH)
    else:
        print(f"Image not found: {IMAGE_PATH}")
