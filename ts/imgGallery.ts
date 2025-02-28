// imageGallery.ts
interface Gallery {
    images: string[];
    currentIndex: number;
}

const galleries: Record<string, Gallery> = {
    gallery: { images: [], currentIndex: 0 },
    inference: { images: [], currentIndex: 0 }
};

// Loads images from the server for a specified gallery
export function loadImages(apiEndpoint: string, galleryId: string): void {
    fetch(apiEndpoint)
        .then(response => response.json())
        .then((data: { images: string[] }) => {
            if (data.images && data.images.length > 0) {
                galleries[galleryId].images = data.images;
                galleries[galleryId].currentIndex = 0; // Reset index when new images are loaded
                displayImage(galleryId);
            } else {
                console.error("❌ No images found at:", apiEndpoint);
            }
        })
        .catch(error => console.error("❌ Error fetching images from", apiEndpoint, ":", error));
}

// Displays the current image in a specified gallery
export function displayImage(galleryId: string): void {
    const gallery = document.getElementById(galleryId);
    if (!gallery) {
        console.error(`❌ Gallery element with ID "${galleryId}" not found.`);
        return;
    }

    const galleryInfo = galleries[galleryId];
    gallery.innerHTML = ""; // Clears the current content

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

// Changes the displayed image in a specified gallery based on direction
export function changeImage(direction: number, galleryId: string): void {
    const galleryInfo = galleries[galleryId];
    galleryInfo.currentIndex = (galleryInfo.currentIndex + direction + galleryInfo.images.length) % galleryInfo.images.length;
    displayImage(galleryId);
}

// Run on page load
document.addEventListener("DOMContentLoaded", function () {
    loadImages('/RunTest_Images', 'RunTest');
});
