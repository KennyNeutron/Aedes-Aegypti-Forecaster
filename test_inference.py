import subprocess
import time
import os
import requests

# Define constants
API_KEY = "122aOY67jDoRdfvlcYg6"
MODEL_ID = "mosquito_annotation/11"
IMAGE_PATH = "images/sample_0001.jpg"


# Check if the server is running
def is_server_running():
    try:
        response = requests.get("http://localhost:9001")
        return response.status_code == 200
    except requests.ConnectionError:
        return False


# Wait for the server to start
def wait_for_server():
    print("Waiting for server to start...")
    for _ in range(20):  # Wait up to 20 seconds
        if is_server_running():
            print("Server is running!")
            return
        time.sleep(1)
    raise RuntimeError("Inference server failed to start.")


# Install Inference CLI
def install_inference_cli():
    print("Installing inference-cli...")
    try:
        subprocess.run(["pip", "install", "inference-cli"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing inference-cli: {e}")
        raise


# Start the inference server
def start_inference_server():
    if is_server_running():
        print("Inference server is already running.")
        return None
    print("Starting inference server...")
    process = subprocess.Popen(
        ["inference", "server", "start"],
        stdout=subprocess.DEVNULL,  # Redirect logs if needed
        stderr=subprocess.DEVNULL,
    )
    wait_for_server()
    return process


# Run inference
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
            print(result.stdout)
        else:
            print("Error during inference:")
            print(result.stderr)
    except Exception as e:
        print(f"Error running inference: {e}")


# Stop the inference server
def stop_inference_server(server_process):
    if server_process:
        print("Stopping inference server...")
        server_process.terminate()
        server_process.wait()
    else:
        print("No server process to stop.")


# Main workflow
if __name__ == "__main__":
    try:
        install_inference_cli()
        server_process = start_inference_server()
        if os.path.exists(IMAGE_PATH):
            run_inference(IMAGE_PATH)
        else:
            print(f"Image not found: {IMAGE_PATH}")
    finally:
        stop_inference_server(server_process if "server_process" in locals() else None)
