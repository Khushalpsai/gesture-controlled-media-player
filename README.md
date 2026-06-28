# Gesture Controlled Media Player

Control your media player using hand gestures — no keyboard, no mouse, just your hand in front of a webcam.

Built with Python, MediaPipe, and OpenCV. Works system-wide with any media player (Spotify, YouTube, VLC, etc).

## Gestures

| Gesture | Action |
|---|---|
| ✊ Fist | Play / Pause |
| 🖐 Open Hand | Stop |
| 👍 Thumbs Up | Volume Up |
| ☝️ Pointing (index finger) | Next Track |
| ✌️ Peace Sign | Previous Track |

## How It Works
1. Webcam captures a live video feed
2. MediaPipe detects hand landmarks in real time
3. Finger states are analysed to identify the gesture
4. A debounce + stability check filters out accidental triggers
5. The matched gesture fires a system-wide media key via pyautogui

## Tech Stack

- **Python 3.11** (using older version of python run in virtual environment because of mediapipe issues)
- **MediaPipe** — hand landmark detection
- **OpenCV** — webcam feed and visual overlay
- **pyautogui** — system media key control

## Project Structure

```
gesture-controlled-media-player/
│
├── main.py                  # Entry point
├── hand_detection.py        # Hand landmarks and gesture labelling
├── gesture_recognition.py   # Debounce and stability logic
├── media_controller.py      # Media key actions
├── requirements.txt         # Dependencies
└── README.md
```

---

## Setup

**1. Clone the repo**
```
git clone https://github.com/Khushalpsai/gesture-controlled-media-player.git
cd gesture-controlled-media-player
```

**2. Create a virtual environment**
```
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```
pip install -r requirements.txt
```

**4. Run**
```
python main.py
```

Press `q` to quit.



## Status

- [x] Phase 1 — Hand detection and gesture recognition
- [x] Phase 2 — Gesture-to-action mapping with debounce and stability
- [ ] Phase 3 — UI overlay and config
- [ ] Phase 4 — Icons and visual feedback
- [ ] Phase 5 — Final polish and packaging



## Author

Khushal — [GitHub](https://github.com/Khushalpsai)