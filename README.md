# AI Virtual Mouse

A Python application that lets you control your computer's mouse using hand gestures in real time.

## Features

- Hand tracking using MediaPipe
- Cursor movement using your index finger
- Mouse clicking with a pinch gesture
- Real-time webcam tracking
- Smooth cursor movement

## Technologies

- Python
- OpenCV
- MediaPipe
- PyAutoGUI

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-virtual-mouse.git
   cd ai-virtual-mouse
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Download the [Hand Landmarker model](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task) and place it inside the `assets` folder.

## Usage

Run the application:

```bash
python main.py
```

- **P** — Pause or resume mouse control
- **Q** — Quit the application
- **Pinch** — Click using your thumb and index finger

## Requirements

- Python 3.14.2 (development environment)
- A webcam
- Windows or another compatible desktop environment

## Future Improvements

- Add more hand gestures
- Improve cursor accuracy
- Add gesture customization

## Author

**Hamza Lamkhailif**

[GitHub](https://github.com/hamza-lamkhailif) · [Portfolio](https://hamzalamkhailif.cloud)
