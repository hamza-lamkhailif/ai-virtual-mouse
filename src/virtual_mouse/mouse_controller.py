import pyautogui


class MouseController:
    def __init__(self):
        # Keep PyAutoGUI's corner failsafe enabled.
        pyautogui.FAILSAFE = True

    def move_to(self, x: int, y: int):
        pyautogui.moveTo(x, y, _pause=False)

    def left_click(self):
        pyautogui.click(_pause=False)
