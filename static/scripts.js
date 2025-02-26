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
