from inference_sdk import InferenceHTTPClient

# Set up the Roboflow API client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com", api_key="122aOY67jDoRdfvlcYg6"
)

# Specify your image file path
image_path = "path/to/your/image.jpg"  # Replace with the actual image path

# Run inference
result = CLIENT.infer(image_path, model_id="mosquito_annotation/11")

# Print the result
print(result)
