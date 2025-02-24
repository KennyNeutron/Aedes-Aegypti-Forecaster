import subprocess
import time
import os
import requests
import json
import cv2


API_KEY = "122aOY67jDoRdfvlcYg6"
MODEL_ID = "mosquito_custom/2"
IMAGE_PATH = "images/sample_0002.jpg"
OUTPUT_IMAGE_PATH = "images/output.jpg"


# Run inference and visualize predictions
def run_inference(image_path):
    print(f"Running inference on {image_path}...")
    try:
        result = subprocess.run(
            [
                "inference",
                "infer",
                "--input",
                image_path,
                "--api-key",
                API_KEY,
                "--model_id",
                MODEL_ID,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            print("Inference successful:")
            raw_output = result.stdout.strip()
            print(f"Raw Output:\n{raw_output}")

            # Extract the JSON portion from the response
            json_data = extract_json(raw_output)
            if json_data:
                predictions = json_data.get("predictions", [])
                print(
                    f"Total FAA detected: {len(predictions)}"
                )  # Print count of FAA detections
                visualize_predictions(image_path, predictions)
            else:
                print("Error: No valid JSON data found in the response.")
        else:
            print("Error during inference:")
            print(result.stderr)
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}")
    except Exception as e:
        print(f"Error running inference: {e}")


# Function to extract JSON from mixed output
def extract_json(raw_output):
    try:
        # Find the start and end indices of the JSON portion
        json_start_index = raw_output.find("{")
        if json_start_index != -1:
            json_end_index = raw_output.rfind("}") + 1
            json_string = raw_output[json_start_index:json_end_index]

            # Print the extracted JSON string for debugging
            print("Extracted JSON string:", json_string)

            # Replace single quotes with double quotes for valid JSON
            json_string = json_string.replace("'", '"')

            return json.loads(json_string)
        else:
            print("No JSON found in the raw output.")
            return None
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return None


# Visualize predictions on the image
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
    try:
        if os.path.exists(IMAGE_PATH):
            # Run inference on the original image
            run_inference(IMAGE_PATH)
        else:
            print(f"Image not found: {IMAGE_PATH}")
    except Exception as e:
        print(f"Unexpected error: {e}")
