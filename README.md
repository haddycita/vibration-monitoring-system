# vibration-monitoring-system
Real-time vibration monitoring system using an ESP32 and MPU6050 sensor, featuring Python-based data processing, anomaly detection, live web dashboard visualization, and data logging for predictive maintenance applications.
# 📡 Real-Time Vibration Monitoring System

A real-time vibration monitoring system developed using an ESP32 microcontroller and an MPU6050 accelerometer sensor. The project processes vibration data in Python, detects anomalies through statistical analysis, visualizes the information on a web dashboard, and stores measurements for further analysis.

---

## 📖 Project Overview

The purpose of this project is to monitor mechanical vibrations in real time and classify the operating condition of a system into three states:

- 🟢 Normal
- 🟠 Warning
- 🔴 Failure

The system acquires acceleration data from an MPU6050 sensor connected to an ESP32. The measurements are transmitted via serial communication to a Python application, where the data are processed, displayed on a live dashboard, and saved into a CSV file.

This project demonstrates the integration of embedded systems, data processing, web visualization, and basic predictive maintenance concepts.

---

## ✨ Features

- Real-time vibration monitoring
- ESP32 + MPU6050 integration
- Automatic system calibration
- Statistical anomaly detection
- Live web dashboard using Flask
- Interactive vibration graph
- Visual traffic-light status indicator
- Automatic CSV data logging
- 3D-printed enclosure for the ESP32 prototype

---

## 🛠 Hardware

- ESP32 Development Board
- MPU6050 Accelerometer/Gyroscope
- USB Cable
- Computer

---

## 💻 Software

- Arduino IDE
- Python 3
- Flask
- NumPy
- PySerial
- Chart.js

---

## ⚙️ System Architecture

```
MPU6050
    │
    ▼
ESP32
    │
Serial Communication
    │
    ▼
Python Application
    │
    ├── Data Processing
    ├── Statistical Analysis
    ├── Dashboard Visualization
    └── CSV Storage
```

---

## 🚀 How It Works

1. The MPU6050 measures acceleration on the X, Y and Z axes.
2. The ESP32 reads the sensor data.
3. Data are transmitted to the computer through serial communication.
4. Python calculates the vibration magnitude.
5. The system performs an automatic calibration.
6. New measurements are compared with the reference values.
7. The dashboard displays:
   - Current vibration value
   - Live graph
   - System status
8. All measurements are stored in a CSV file.

---

## 📂 Repository Structure

```
.
├── app.py
├── codigo_ESP32.ino
├── README.md
└── datos_vibracion.csv
```

---

## 🎯 Applications

This prototype can serve as a basis for:

- Predictive maintenance
- Machine condition monitoring
- Educational demonstrations
- Mechanical vibration analysis
- IoT monitoring systems

---

## 👩‍💻 Author

**Haddy Velastegui**

Mechanical Engineering Student  
Escuela Politécnica Nacional (Ecuador)

---

## 📜 License

This repository is intended for educational purposes.
