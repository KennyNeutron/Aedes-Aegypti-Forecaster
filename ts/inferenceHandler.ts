// inferenceHandler.ts

// Performs the mosquito detection inference
export function performInference(): void {
    const button = document.querySelector(".button_default") as HTMLButtonElement | null;
    if (!button) return;

    button.disabled = true;
    button.textContent = "Capturing & Processing..."; // UI update

    showNotification("📸 Capturing and running inference...");

    fetch('/RunTest_Capture', { method: 'POST' })
        .then(response => response.json())
        .then((data: { status: string; error?: string }) => {
            if (data.status === "Captured & Inferred") {
                console.log("✅ Image captured and inference completed!");
                showNotification("✅ Image captured & processed! Reloading...");

                setTimeout(() => {
                    location.reload(); // Refresh the page to display the updated image
                }, 2000);
            } else {
                console.error("❌ Error:", data.error);
                showNotification("❌ Error capturing or processing image!", "error");
                button.disabled = false;
                button.textContent = "PERFORM INFERENCE";
            }
        })
        .catch(error => {
            console.error("❌ Fetch Error:", error);
            showNotification("❌ Error communicating with server!", "error");
            button.disabled = false;
            button.textContent = "PERFORM INFERENCE";
        });
}

// Show a notification on the screen
export function showNotification(message: string, type: string = "success"): void {
    const notification: HTMLDivElement = document.createElement("div");
    notification.textContent = message;
    notification.className = `notification ${type}`;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000); // Remove notification after 3 seconds
}

// Ensure event listener runs
document.addEventListener("DOMContentLoaded", function () {
    const testButton = document.querySelector(".button_default");
    if (testButton) {
        testButton.addEventListener("click", performInference);
    }
});
