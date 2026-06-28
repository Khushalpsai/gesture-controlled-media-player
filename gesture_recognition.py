import time
from collections import deque
from config import COOLDOWN, STABILITY_COUNT

last_trigger = {} #gesture timestamp
gesture_history = deque(maxlen=STABILITY_COUNT)

def should_trigger(gesture):
    current = time.time()
    if gesture not in last_trigger:
        last_trigger[gesture] = current
        return True
    if current - last_trigger[gesture] >= COOLDOWN:
        last_trigger[gesture] = current
        return True
    return False

def is_stable(gesture):
    gesture_history.append(gesture)
    return gesture_history.count(gesture) == STABILITY_COUNT