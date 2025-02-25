import requests
import matplotlib.pyplot as plt

# Use the same API key from your inference script
API_KEY = "122aOY67jDoRdfvlcYg6"
PROJECT_ID = "mosquito_custom"  # Your Roboflow project ID
MODEL_VERSION = "2"  # Update with the correct model version

# Roboflow Training Metrics API Endpoint
API_URL = (
    f"https://api.roboflow.com/{PROJECT_ID}/{MODEL_VERSION}/metrics?api_key={API_KEY}"
)


def fetch_training_metrics():
    """Fetch training metrics from Roboflow API."""
    response = requests.get(API_URL)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error: Failed to fetch data (Status {response.status_code})")
        return None


def plot_training_graph(metrics):
    """Plot the training progress graph."""
    if not metrics or "epochs" not in metrics:
        print("❌ No training data available.")
        return

    epochs = metrics["epochs"]
    losses = metrics["loss"]
    accuracies = metrics.get(
        "accuracy", [None] * len(epochs)
    )  # Some models may not return accuracy

    # Plot Loss
    plt.figure(figsize=(8, 5))
    plt.plot(epochs, losses, label="Loss", marker="o", linestyle="-", color="red")

    # Plot Accuracy (if available)
    if any(accuracies):  # Check if accuracy data exists
        plt.plot(
            epochs,
            accuracies,
            label="Accuracy",
            marker="s",
            linestyle="--",
            color="blue",
        )

    # Formatting the graph
    plt.xlabel("Epochs")
    plt.ylabel("Metrics")
    plt.title("Roboflow Model Training Progress")
    plt.legend()
    plt.grid(True)
    plt.show()


# Fetch and plot training graph
metrics = fetch_training_metrics()
if metrics:
    plot_training_graph(metrics)
