import cv2
import mediapipe as mp
import time

# Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

# Hand Landmarks
# Fingertip IDs and MCP (knuckle) base IDs for more stable comparison
FINGERTIPS = [4, 8, 12, 16, 20]
FINGERBASE = [2, 5, 9, 13, 17]  # MCP joints — more stable than DIP


def count_raised_fingers(hand_landmarks, hand_label):
    landmarks = hand_landmarks.landmark
    raised = []

    # Thumb: compare x-axis (moves sideways, not up/down)
    # Direction depends on which hand it is (after frame flip)
    if hand_label == "Right":
        raised.append(landmarks[FINGERTIPS[0]].x < landmarks[FINGERBASE[0]].x)
    else:
        raised.append(landmarks[FINGERTIPS[0]].x > landmarks[FINGERBASE[0]].x)

    # Other 4 fingers: tip higher (smaller y) than knuckle = raised
    for tip, base in zip(FINGERTIPS[1:], FINGERBASE[1:]):
        raised.append(landmarks[tip].y < landmarks[base].y)

    return raised


def get_gesture_label(raised):
    thumb, index, middle, ring, pinky = raised
    total = sum(raised)

    if total == 0:
        return "FIST - Pause/Play"
    elif total == 5:
        return "OPEN HAND - Stop"
    elif thumb and not index and not middle and not ring and not pinky:
        return "THUMBS UP - Vol Up"
    elif not thumb and index and not middle and not ring and not pinky:
        return "POINTING - Next Track"
    elif not thumb and index and middle and not ring and not pinky:
        return "PEACE - Previous Track"
    else:
        return "..."


def hud(frame, gesture, fps, finger_states):
    h, w = frame.shape[:2]

    # Semi-transparent green bar at bottom
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - 90), (w, h), (0, 255, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Gesture label
    color = (0, 0, 0) if gesture != "..." else (200, 100, 100)
    cv2.putText(frame, gesture, (10, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # FPS counter
    cv2.putText(frame, f"FPS: {int(fps)}", (w - 110, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

    # Finger state dots (T I M R P)
    labels = ["T", "I", "M", "R", "P"]
    for i, (label, state) in enumerate(zip(labels, finger_states)):
        x = 20 + i * 36
        y = h - 18
        dot_color = (100, 220, 100) if state else (180, 180, 180)
        cv2.circle(frame, (x, y), 10, dot_color, -1)
        cv2.putText(frame, label, (x - 5, y + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Gesture legend (top right)
    legend = [
        "FIST - Pause/Play",
        "OPEN HAND - Stop",
        "THUMBS UP - Vol Up",
        "POINTING - Next Track",
        "PEACE - Previous Track",
    ]
    for i, line in enumerate(legend):
        cv2.putText(frame, line, (w - 260, 60 + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)