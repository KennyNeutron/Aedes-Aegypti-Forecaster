// Maintains the state of image galleries.
const galleries = {
    'gallery': {
        images: [],
        currentIndex: 0
    },
    'inference': {
        images: [],
        currentIndex: 0
    }
};

// Updates the display data on the home page.
function updateData() {
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            let splitDateTime = data.time.split(" ");
            document.getElementById("time").textContent = splitDateTime[1];
            document.getElementById("date").textContent = splitDateTime[0];
            document.getElementById("temperature").textContent = data.temperature.toFixed(2);

            let currentHour = parseInt(splitDateTime[1].split(":")[0]);
            let nextCapture = currentHour >= 20 ? "07:00 AM (Tomorrow)" :
                              currentHour >= 7 ? "08:00 PM" : "07:00 AM";
            document.getElementById("next-capture").textContent = nextCapture;
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Loads images from the server for a specified gallery.
function loadImages(apiEndpoint, galleryId) {
    fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
            if (data.images && data.images.length > 0) {
                galleries[galleryId].images = data.images;
                galleries[galleryId].currentIndex = 0;  // Resets index when images are loaded
                displayImage(galleryId);
            } else {
                console.error("No images found at:", apiEndpoint);
            }
        })
        .catch(error => console.error("Error fetching images from", apiEndpoint, ":", error));
}

// Displays the current image in a specified gallery.
function displayImage(galleryId) {
    const gallery = document.getElementById(galleryId);
    const galleryInfo = galleries[galleryId];
    gallery.innerHTML = "";  // Clears the current content
    if (galleryInfo.images.length > 0) {
        let img = document.createElement("img");
        img.src = galleryInfo.images[galleryInfo.currentIndex];
        img.classList.add("active");
        gallery.appendChild(img);

        let filename = document.createElement("p");
        filename.textContent = "Filename: " + galleryInfo.images[galleryInfo.currentIndex].split('/').pop();
        gallery.appendChild(filename);
    } else {
        gallery.textContent = "No images to display";
    }
}

// Changes the displayed image in a specified gallery based on direction.
function changeImage(direction, galleryId) {
    const galleryInfo = galleries[galleryId];
    galleryInfo.currentIndex = (galleryInfo.currentIndex + direction + galleryInfo.images.length) % galleryInfo.images.length;
    displayImage(galleryId);
}

// Confirms and clears all data in the database.
function clearDatabase() {
    let password = prompt("Enter admin password to clear the database:");
    if (password) {
        fetch('/clear-data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'Database cleared') {
                alert('Database has been cleared.');
                location.reload();
            } else {
                alert(data.status); // Displays error message
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error clearing database.');
        });
    }
}


// Initiates the download of the data log as a CSV file.
function downloadCSV() {
    window.location.href = '/download-data'; // Navigates to download data endpoint
}


document.addEventListener("DOMContentLoaded", function() {
    if (document.getElementById("RunTest")) {
        fetch('/RunTest_Images')
            .then(response => response.json())
            .then(data => {
                console.log("Received image data:", data);
                const gallery = document.getElementById('RunTest');
                gallery.innerHTML = "";

                if (data.images.length > 0) {
                    let img = document.createElement("img");
                    img.src = data.images[0];
                    img.classList.add("active");
                    gallery.appendChild(img);

                    let filename = document.createElement("p");
                    filename.textContent = "Filename: " + data.images[0].split('/').pop();
                    gallery.appendChild(filename);
                } else {
                    gallery.textContent = "No image available";
                }
            })
            .catch(error => console.error("Error fetching RunTest image:", error));
    }
});

function performInference() {
    const button = document.querySelector(".button_default");
    button.disabled = true;
    button.textContent = "Capturing & Processing...";  // Update UI to show processing state

    showNotification("📸 Capturing and running inference...");

    fetch('/RunTest_Capture', { method: 'POST' })  // Run capture and inference
        .then(response => response.json())
        .then(data => {
            if (data.status === "Captured & Inferred") {
                console.log("✅ Image captured and inference completed!");
                showNotification("✅ Image captured & processed! Reloading...");

                setTimeout(() => {
                    location.reload();  // Refresh the page to display the updated image
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
function showNotification(message, type = "success") {
    const notification = document.createElement("div");
    notification.textContent = message;
    notification.className = `notification ${type}`;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);  // Remove notification after 3 seconds
}