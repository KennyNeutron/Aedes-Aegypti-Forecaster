# Aedes Aegypti Forecaster

## Project Overview

The **Aedes Aegypti Forecaster** is an AI-powered mosquito tracking system that uses image recognition to count female Aedes aegypti mosquitoes. The system is designed to predict mosquito populations based on environmental factors like temperature. The project runs on a **Raspberry Pi 4 Model B (8GB RAM)**, utilizing **a Raspberry Pi Camera Module v2** and **a DS3231 RTC sensor** for timestamped data collection.

## Features

- **Automated Mosquito Counting**: Uses Roboflow-trained YOLO model for mosquito detection.
- **Scheduled Image Capture**: Takes pictures twice a day (7 AM & 8 PM) using the Raspberry Pi Camera Module v2.
- **Temperature Logging**: DS3231 sensor records ambient temperature and syncs time.
- **Data Storage & Prediction**: Logs mosquito counts and temperature in a **MySQL database**.
- **Web-Based Dashboard**: Frontend with **HTML, JavaScript, and CSS** to display captured data.
- **Flask Backend**: Manages image processing, inference, and API communications.
- **Inference Testing**: Allows users to test mosquito detection manually via a web interface.

## Project Structure

```
Aedes-Agypti-Forecaster/
│── backend/
│   ├── main.py                     # Core backend logic (image capture, inference, scheduling, database logging)
│   ├── synctime.py                 # Syncs Raspberry Pi time with DS3231 RTC
│   ├── DS3231_SetTime.py           # Sets DS3231 RTC time
│   ├── inference.py                # Runs inference on locally stored images
│   ├── inference_hosted_api.py     # Uses Roboflow's hosted API for inference
│   ├── setup_database.py           # Initializes MySQL database tables
│   ├── gpio_control.py             # Handles GPIO interactions for external components
│── frontend/
│   ├── templates/
│   │   ├── index.html              # Main dashboard page
│   │   ├── base.html               # UI layout template
│   │   ├── gallery.html            # Displays captured mosquito images
│   │   ├── inference.html          # Shows mosquito detection results
│   │   ├── data_log.html           # Displays mosquito count logs
│   │   ├── RunTest.html            # Test page for inference
│   ├── static/
│   │   ├── scripts.js              # Handles frontend logic and API interactions
│   │   ├── styles.css              # Styles for web interface
|   ├── ts/
│   │   ├── dataFetcher.ts          # Handles data fetching for frontend logic and API interactions
│   │   ├── imgGallery.ts           # Handles data fetching for gallery images
│   │   ├── inferenceHandler.ts     # Handles data fetching for the inferences
│   │   ├── scripts.ts              # TS code for the script for generating scripts.js
│── hardware/
│   ├── 3D Design/                  # 3D enclosure models for Raspberry Pi case
│── archive/                        # Older versions and experimental scripts
│── requirements.txt                # Dependencies for running the project
│── README.md                       # Project documentation
```

## Installation

### Prerequisites

- **Raspberry Pi 4 Model B (8GB RAM)**
- **Raspberry Pi Camera Module v2**
- **DS3231 RTC Module**
- **MySQL Database**
- **Python 3.10+**

### Setup

1. **Clone the repository**:

   ```sh
   git clone https://github.com/KennyNeutron/Aedes-Agypti-Forecaster.git
   cd Aedes-Agypti-Forecaster
   ```

2. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

3. **Setup MySQL database**:

   ```sh
   python setup_database.py
   ```

4. **Run the backend**:

   ```sh
   python main.py
   ```

5. **Access the web interface**:
   Open a browser and go to `http://localhost:5000`.

## Data Prediction

Using **linear regression**, the system predicts mosquito populations based on **temperature trends** over 15 days. This is visualized in an analytics dashboard.

## Future Improvements

- Add **real-time mosquito classification**
- Implement **SMS/email alerts** for mosquito surges
- Integrate **climate-based forecasting models**

## License

This project is under the MIT License.

---

_Last updated: March 2025_
