# Aedes aegypti Forecaster

The **Aedes aegypti Forecaster** is a smart mosquito trap system designed to detect, count, and log **female Aedes aegypti mosquitoes** using a **Raspberry Pi 4 Model B (8GB RAM)**, **Raspberry Pi Camera Module v2**, and a **DS3231 Real-Time Clock (RTC)**. The system uses **computer vision** powered by **Roboflow** for mosquito detection and logs data in an **SQLite database**.

## Features

- 📸 **Automated Image Capture**: Captures images at **7:00 AM and 8:00 PM** daily.
- 🦟 **Mosquito Detection & Counting**: Uses **Roboflow's AI model** to identify and count **female Aedes aegypti mosquitoes**.
- 🌡 **Temperature Logging**: Records **ambient temperature** from the **DS3231 RTC**.
- 🗂 **Data Logging**: Saves detected mosquito count and temperature readings to an **SQLite database**.
- 📊 **Web Dashboard**: A **Flask-based web interface** for viewing **captured images, inference results, and logged data**.
- 📥 **CSV Export & Database Management**: Supports **downloading mosquito count logs** and clearing the database.
- 🎨 **Dark-Themed UI**: Stylish, responsive **web interface** with easy navigation.

---

## System Overview

### 🏗 Hardware Components

- **Raspberry Pi 4 Model B (8GB RAM)**
- **Raspberry Pi Camera Module v2**
- **DS3231 Real-Time Clock (RTC)**
- **Sticky Paper Trap**
- **Enclosure (3D Printed)**

### 🖥 Software & Libraries

- **Python (Flask, OpenCV, NumPy, Requests)**
- **SQLite (Data Logging)**
- **Roboflow API (Inference)**
- **JavaScript (Frontend Interactions)**
- **HTML + CSS (User Interface)**

---

## 📌 Installation Guide

### 1️⃣ Prerequisites

Ensure your **Raspberry Pi 4** is set up with:

- **Raspberry Pi OS (64-bit)**
- **Python 3.x**
- **Flask Framework**
- **Required Dependencies** (see `requirements.txt`)

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python main.py
```

The application runs on **http://0.0.0.0:5000**.

---

## 🌍 Web Interface

The system provides an interactive **Flask-based web dashboard** with the following features:

### 📷 **Home Page**
- Displays **current date & temperature**.
- Shows **next scheduled image capture**.

### 🖼 **Gallery**
- View **all captured images**.

### 🔬 **Inference**
- Displays processed images with **mosquito detection results**.

### 📊 **Data Log**
- Shows recorded **mosquito count and temperature**.
- Provides **CSV export** and **database clear** options.

---

## 🛠 Code Structure

```
📂 project_root/
├── 📄 main.py          # Flask application backend
├── 📂 templates/       # HTML templates for web UI
│   ├── 📄 base.html
│   ├── 📄 index.html
│   ├── 📄 gallery.html
│   ├── 📄 inference.html
│   ├── 📄 data_log.html
├── 📂 static/          # CSS, JavaScript, and images
│   ├── 📄 styles.css
│   ├── 📄 scripts.js
│   ├── 📂 images/
├── 📂 captured_images/  # Stored captured images
├── 📂 inference_output/ # Processed images with bounding boxes
├── 📄 FAA_DB.db        # SQLite database
├── 📄 requirements.txt # Required dependencies
```

---

## 🏆 Acknowledgments

- **Raspberry Pi Foundation** - For the computing power.
- **Roboflow** - For providing the **Mosquito Detection Model**.
- **Adafruit** - For the **DS3231 RTC Module**.
- **Flask Community** - For the **web framework**.

---
