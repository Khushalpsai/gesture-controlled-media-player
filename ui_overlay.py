import cv2
from config import *

def hud(frame, gesture, fps, finger_states):
    h, w = frame.shape[:2]

    # Semi-transparent green bar at bottom
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - 90), (w, h), HUD_BAR_COLOUR, -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Gesture label
    color = HUD_GESTURE_COLOUR if gesture != "..." else HUD_UNKNOWN_COLOUR
    cv2.putText(frame, gesture, (10, h - 50), cv2.FONT_HERSHEY_SIMPLEX, HUD_GESTURE_FONT_SCALE, color, 2)

    # FPS counter
    cv2.putText(frame, f"FPS: {int(fps)}", (w - 110, 30),
                cv2.FONT_HERSHEY_SIMPLEX, HUD_FPS_FONT_SCALE, HUD_FPS_COLOUR, 1, cv2.LINE_AA)

    # Finger state dots (T I M R P)
    labels = ["T", "I", "M", "R", "P"]
    for i, (label, state) in enumerate(zip(labels, finger_states)):
        x = 20 + i * 36
        y = h - 18
        dot_color = DOT_ACTIVE_COLOUR if state else DOT_INACTIVE_COLOUR
        cv2.circle(frame, (x, y), 10, dot_color, -1)
        cv2.putText(frame, label, (x - 5, y + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, HUD_SMALL_FONT_SCALE, DOT_LABEL_COLOUR, 1)

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
                    cv2.FONT_HERSHEY_SIMPLEX, HUD_SMALL_FONT_SCALE, LEGEND_COLOUR, 1)