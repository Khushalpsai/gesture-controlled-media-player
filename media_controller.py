import pyautogui


def perform_action(gesture):
    if gesture == "FIST - Pause/Play":
        pyautogui.press('playpause')
    elif gesture == "OPEN HAND - Stop":
        pyautogui.press('stop')
    elif gesture == "THUMBS UP - Vol Up":
        pyautogui.press('volumeup')
    elif gesture == "POINTING - Next Track":
        pyautogui.press('nexttrack')
    elif gesture == "PEACE - Previous Track":
        pyautogui.press('prevtrack')
    else:
        print("Unknown gesture:", gesture)