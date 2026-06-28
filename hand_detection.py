import cv2
import mediapipe as mp
import time

from config import DETECTION_CONFIDENCE, MAX_HANDS, TRACKING_CONFIDENCE

# Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=MAX_HANDS,
    min_detection_confidence= DETECTION_CONFIDENCE,
    min_tracking_confidence= TRACKING_CONFIDENCE
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


