# WGS Technical Test Submission

This repository contains the source code for three distinct technical projects as part of the WGS technical test submission. Each project addresses a specific domain: Web Development (CMS), Artificial Intelligence (Object Detection), and IoT/Computer Vision (Camera Control).

## 📁 Repository Structure & Projects Summary

Below is a brief overview of each project included in this repository. Please follow the links to their respective detailed documentation for setup instructions and further details.

### 1. Simple CMS Purchase Simulation
**Path:** [`content-management-system/`](./content-management-system)

A basic Content Management System built using **PHP CodeIgniter 4 (MVC architecture)**. It simulates a product purchasing workflow without requiring authentication or authorization.
- **Key Features:** Admin panel for managing Categories, Products, and Orders (CRUD). A Frontend Shop catalog that allows adding products to a cart, checking out, and automatically deducting stock.
- **Tech Stack:** PHP 8.2+, CodeIgniter 4, MySQL, Bootstrap 5.
- **Documentation:** [View Full CMS Documentation](./content-management-system/README.md)

---

### 2. AI Fruit Object Detection
**Path:** [`ai-object-detection/`](./ai-object-detection)

An AI-powered computer vision model trained to detect and classify specific fruits (Apples, Bananas, and Oranges) in images. This project utilizes the state-of-the-art **YOLOv8** architecture.
- **Key Features:** Custom dataset preparation script, YOLOv8 model training pipeline, and an inference script to draw bounding boxes and confidence scores on newly provided images.
- **Tech Stack:** Python 3, Ultralytics (YOLOv8), OpenCV.
- **Documentation:** [View Full AI Object Detection Documentation](./ai-object-detection/README.MD)

---

### 3. Camera Control IoT Script
**Path:** [`camera-control-iot/`](./camera-control-iot)

A lightweight Python script designed for local camera interaction and control using **OpenCV**. It provides basic and advanced image capture features directly from a connected webcam.
- **Key Features:** Live camera preview, Single Capture mode via keyboard shortcut, and an advanced Burst Capture mode for continuous shooting while holding down a specific key. Configurable camera parameters.
- **Tech Stack:** Python 3, OpenCV (`cv2`), Keyboard listener library.
- **Documentation:** [View Full Camera Control Documentation](./camera-control-iot/README.md)

## 🚀 Getting Started

To get started with any of the projects, please navigate into the respective project directory and refer to its documentation link provided above. Each sub-project has its own independent setup steps, dependency list, and execution environments.

---

## 💻 System Specifications

As required for this submission, below are the hardware and operating system specifications of the machine used during the development and testing of these projects:

- **Operating System:** Microsoft Windows 11 Home Single Language
- **Processor (CPU):** Intel(R) Core(TM) i7-8750H CPU @ 2.20GHz
- **Memory (RAM):** 24 GB
- **Graphics (GPU):** NVIDIA GeForce GTX 1050 Ti / Intel(R) UHD Graphics 630
