import cv2
import time
from config import FRAME_WIDTH, FRAME_HEIGHT
from gesture_recognition import is_stable, should_trigger
from media_controller import perform_action
from hand_detection import hands, mp_draw, mp_styles, mp_hands, count_raised_fingers, get_gesture_label
from ui_overlay import hud


last_action_time = 0


# Main loop
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

prev_time = time.time()
print("Starting hand gesture recognition. Press 'q' to exit.")

gesture = "..."
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror the frame so it feels natural
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    finger_states = [False] * 5
    gesture = "..."

    if results.multi_hand_landmarks and results.multi_handedness:
        hand_lm = results.multi_hand_landmarks[0]
        hand_label = results.multi_handedness[0].classification[0].label  # "Left" or "Right"

        mp_draw.draw_landmarks(
            frame, hand_lm, mp_hands.HAND_CONNECTIONS,
            mp_styles.get_default_hand_landmarks_style(),
            mp_styles.get_default_hand_connections_style()
        )

        finger_states = count_raised_fingers(hand_lm, hand_label)
        gesture = get_gesture_label(finger_states)
        if is_stable(gesture) and should_trigger(gesture):
            perform_action(gesture)
            last_action_time = time.time()  # Update the last action time

    # FPS calculation
    now = time.time()
    fps = 1 / (now - prev_time)
    prev_time = now

    hud(frame, gesture, fps, finger_states, last_action_time)
    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()