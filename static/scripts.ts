/* 
Maintains the state of image galleries.
*/
interface Gallery {
    images: string[];
    currentIndex: number;
}

interface Galleries {
    [key: string]: Gallery;
}

const galleries: Galleries = {
    'gallery': {
        images: [],
        currentIndex: 0
    },
    'inference': {
        images: [],
        currentIndex: 0
    }
};

/* 
Updates the display data on the home page.
*/
function updateData(): void {
    fetch("/data")
        .then(response => response.json())
        .then((data: { time: string; temperature: number }) => {
            let splitDateTime: string[] = data.time.split(" ");
            document.getElementById("time")!.textContent = splitDateTime[1];
            document.getElementById("date")!.textContent = splitDateTime[0];
            document.getElementById("temperature")!.textContent = data.temperature.toFixed(2);

            let currentHour: number = parseInt(splitDateTime[1].split(":")[0]);
            let nextCapture: string = currentHour >= 20 ? "07:00 AM (Tomorrow)" :
                              currentHour >= 7 ? "08:00 PM" : "07:00 AM";
            document.getElementById("next-capture")!.textContent = nextCapture;
        })
        .catch(error => console.error("Error fetching data:", error));
}

/* 
Loads images from the server for a specified gallery.
*/
function loadImages(apiEndpoint: string, galleryId: string): void {
    fetch(apiEndpoint)
        .then(response => response.json())
        .then((data: { images: string[] }) => {
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

/* 
Displays the current image in a specified gallery.
*/
function displayImage(galleryId: string): void {
    const gallery: HTMLElement = document.getElementById(galleryId)!;
    const galleryInfo: Gallery = galleries[galleryId];
    gallery.innerHTML = "";  // Clears the current content
    if (galleryInfo.images.length > 0) {
        let img: HTMLImageElement = document.createElement("img");
        img.src = galleryInfo.images[galleryInfo.currentIndex];
        img.classList.add("active");
        gallery.appendChild(img);

        let filename: HTMLParagraphElement = document.createElement("p");
        filename.textContent = "Filename: " + galleryInfo.images[galleryInfo.currentIndex].split('/').pop();
        gallery.appendChild(filename);
    } else {
        gallery.textContent = "No images to display";
    }
}

/* 
Changes the displayed image in a specified gallery based on direction.
*/
function changeImage(direction: number, galleryId: string): void {
    const galleryInfo: Gallery = galleries[galleryId];
    galleryInfo.currentIndex = (galleryInfo.currentIndex + direction + galleryInfo.images.length) % galleryInfo.images.length;
    displayImage(galleryId);
}

/* 
Confirms and clears all data in the database.
*/
function clearDatabase(): void {
    let password: string | null = prompt("Enter admin password to clear the database:");
    if (password) {
        fetch('/clear-data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: password })
        })
        .then(response => response.json())
        .then((data: { status: string }) => {
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

/* 
Initiates the download of the data log as a CSV file.
*/
function downloadCSV(): void {
    window.location.href = '/download-data'; // Navigates to download data endpoint
}

document.addEventListener("DOMContentLoaded", function(): void {
    if (document.getElementById("RunTest")) {
        fetch('/RunTest_Images')
            .then(response => response.json())
            .then((data: { images: string[] }) => {
                console.log("Received image data:", data);
                const gallery: HTMLElement = document.getElementById('RunTest')!;
                gallery.innerHTML = "";

                if (data.images.length > 0) {
                    let img: HTMLImageElement = document.createElement("img");
                    img.src = data.images[0];
                    img.classList.add("active");
                    gallery.appendChild(img);

                    let filename: HTMLParagraphElement = document.createElement("p");
                    filename.textContent = "Filename: " + data.images[0].split('/').pop();
                    gallery.appendChild(filename);
                } else {
                    gallery.textContent = "No image available";
                }
            })
            .catch(error => console.error("Error fetching RunTest image:", error));
    }
});

function performInference(): void {
    const button: HTMLButtonElement = document.querySelector(".button_default") as HTMLButtonElement;
    button.disabled = true;
    button.textContent = "Capturing & Processing...";  // Update UI to show processing state

    showNotification("📸 Capturing and running inference...");

    fetch('/RunTest_Capture', { method: 'POST' })  // Run capture and inference
        .then(response => response.json())
        .then((data: { status: string; error?: string }) => {
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

/* 
Show a notification on the screen
*/
function showNotification(message: string, type: string = "success"): void {
    const notification: HTMLDivElement = document.createElement("div");
    notification.textContent = message;
    notification.className = `notification ${type}`;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);  // Remove notification after 3 seconds
}
