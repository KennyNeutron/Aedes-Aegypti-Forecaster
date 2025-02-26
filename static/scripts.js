// Object to keep track of state for each gallery
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

// Function to update the data on the home page
function updateData() {
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            let splitDateTime = data.time.split(" ");
            document.getElementById("time").textContent = splitDateTime[1];
            document.getElementById("date").textContent = splitDateTime[0];
            document.getElementById("temperature").textContent = data.temperature.toFixed(2);

            let currentHour = parseInt(splitDateTime[1].split(":")[0]);
            let nextCapture;
            if (currentHour >= 20) {
                nextCapture = "07:00 AM (Tomorrow)";
            } else if (currentHour >= 7) {
                nextCapture = "08:00 PM";
            } else {
                nextCapture = "07:00 AM";
            }
            document.getElementById("next-capture").textContent = nextCapture;
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Function to load images from server
function loadImages(apiEndpoint, galleryId) {
    fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
            if (data.images && data.images.length > 0) {
                galleries[galleryId].images = data.images;
                galleries[galleryId].currentIndex = 0;  // Reset index whenever images are loaded
                displayImage(galleryId);
            } else {
                console.error("No images found at:", apiEndpoint);
            }
        })
        .catch(error => {
            console.error("Error fetching images from", apiEndpoint, ":", error);
        });
}

// Function to display the current image in the gallery
function displayImage(galleryId) {
    const gallery = document.getElementById(galleryId);
    const galleryInfo = galleries[galleryId];
    gallery.innerHTML = "";  // Clear current content
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

// Function to change image in the gallery
function changeImage(direction, galleryId) {
    const galleryInfo = galleries[galleryId];
    const len = galleryInfo.images.length;
    galleryInfo.currentIndex = (galleryInfo.currentIndex + direction + len) % len;
    displayImage(galleryId);
}
