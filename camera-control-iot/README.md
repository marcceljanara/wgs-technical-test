# Camera Control IoT - Premium Dashboard

A desktop-based graphical dashboard application for interfacing with connected cameras (webcams) using **Python**, **OpenCV**, and **Tkinter**. This tool is designed as a lightweight interface for capturing images in IoT environments.

## ✨ Features

- **Live Camera Preview:** Smooth real-time video feed rendering.
- **Hardware Selection:** Easily switch between multiple connected camera devices.
- **Parameter Control:**
  - Adjustable Resolution (VGA, HD, FHD)
  - Auto/Manual Exposure control (Shutter speed)
  - Gain control (ISO equivalent)
- **Capture Modes:**
  - **Single Capture:** Press `C` or click the button to capture a single frame.
  - **Burst Capture:** Hold `B` or `Space`, or click and hold the button to capture multiple frames continuously.
- **Visual Feedback:** Flashing screen effects on capture and live status indicators.

## 🛠️ Technical Stack

- **Python 3.x**
- **OpenCV (`cv2`)**: For interfacing with hardware cameras and extracting frames.
- **Tkinter & ttk**: For building the native, responsive GUI.
- **Pillow (`PIL`)**: For image processing and formatting between OpenCV and Tkinter.

## 🚀 Setup & Installation

1. Navigate to the project directory:
   ```bash
   cd camera-control-iot
   ```
2. (Optional but recommended) Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

Run the main application script:

```bash
python main.py
```

### Hotkeys
- **`C`**: Take a single photo.
- **`B`** or **`Space`** (Hold): Burst capture mode (takes photos rapidly until released).

### Outputs
All captured images are automatically saved with a timestamp in the auto-generated `captures/` folder within the project directory.
