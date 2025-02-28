// dataFetcher.ts
interface DataResponse {
    time: string;
    temperature: number;
}

// Updates the display data on the home page
export function updateData(): void {
    fetch("/data")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then((data: DataResponse) => {
            console.log("✅ Data received:", data);

            // Get elements safely
            const timeElement = document.getElementById("time");
            const dateElement = document.getElementById("date");
            const temperatureElement = document.getElementById("temperature");
            const nextCaptureElement = document.getElementById("next-capture");

            if (!timeElement || !dateElement || !temperatureElement || !nextCaptureElement) {
                console.error("❌ One or more elements not found in the DOM");
                return;
            }

            let [date, time] = data.time.split(" ");
            timeElement.textContent = time;
            dateElement.textContent = date;
            temperatureElement.textContent = data.temperature.toFixed(2);

            let currentHour: number = parseInt(time.split(":")[0], 10);
            let nextCapture: string = currentHour >= 20 ? "07:00 AM (Tomorrow)" :
                                      currentHour >= 7 ? "08:00 PM" : "07:00 AM";

            nextCaptureElement.textContent = nextCapture;
        })
        .catch(error => {
            console.error("❌ Error fetching data:", error);
            alert("⚠️ Failed to load data from server. Check your connection.");
        });
}

// Ensure updateData runs on page load
document.addEventListener("DOMContentLoaded", updateData);
