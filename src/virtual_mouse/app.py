import time

import cv2
import mediapipe as mp
import pyautogui

from .config import AppConfig
from .hand_detector import HandDetector
from .gesture_recognizer import GestureRecognizer
from .cursor_controller import CursorController
from .mouse_controller import MouseController


class VirtualMouseApp:
    def __init__(self, config: AppConfig):
        self.config = config

        self.detector = HandDetector(config)
        self.mouse = MouseController()

        screen_width, screen_height = pyautogui.size()

        self.cursor = CursorController(
            screen_width=screen_width,
            screen_height=screen_height,
            smoothing=config.smoothing,
            margin=config.margin,
        )

        self.gestures = GestureRecognizer(
            config.pinch_threshold
        )

        self.paused = True
        self.previous_pinch = False
        self.last_click_time = 0.0

        self.previous_frame_time = time.perf_counter()
        self.fps = 0.0

        self.connections = (
            mp.tasks.vision.HandLandmarksConnections
            .HAND_CONNECTIONS
        )

    def draw_hand(self, frame, landmarks):
        height, width = frame.shape[:2]
        points = []

        for landmark in landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)

            points.append((x, y))

            cv2.circle(
                frame,
                (x, y),
                4,
                (0, 255, 0),
                cv2.FILLED,
            )

        for connection in self.connections:
            start = points[connection.start]
            end = points[connection.end]

            cv2.line(
                frame,
                start,
                end,
                (255, 0, 255),
                2,
            )

        cv2.line(
            frame,
            points[4],
            points[8],
            (0, 255, 255),
            2,
        )

    def process_hand(self, landmarks, now):
        pinching = self.gestures.is_pinching(landmarks)

        if not self.paused:
            index_tip = landmarks[8]

            x, y = self.cursor.update(
                index_tip.x,
                index_tip.y,
            )

            self.mouse.move_to(x, y)

            # Click only when a new pinch starts.
            if (
                pinching
                and not self.previous_pinch
                and now - self.last_click_time
                >= self.config.click_cooldown
            ):
                self.mouse.left_click()
                self.last_click_time = now

        self.previous_pinch = pinching
        return "PINCH / CLICK" if pinching else "TRACKING"

    def draw_status(self, frame, gesture):
        status = "PAUSED" if self.paused else "ACTIVE"
        color = (0, 0, 255) if self.paused else (0, 200, 0)

        cv2.putText(
            frame,
            f"Mouse: {status}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2,
        )

        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"FPS: {self.fps:.1f} | P: pause/resume | Q: quit",
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 0),
            2,
        )

    def run(self):
        try:
            while True:
                frame, hands = self.detector.read_frame()

                if frame is None:
                    print("Unable to read webcam frame.")
                    break

                now = time.perf_counter()
                delta = now - self.previous_frame_time
                self.previous_frame_time = now

                if delta > 0:
                    instant_fps = 1.0 / delta
                    self.fps = (
                        instant_fps if self.fps == 0
                        else 0.9 * self.fps + 0.1 * instant_fps
                    )

                gesture = "NO HAND"

                if hands:
                    landmarks = hands[0]
                    self.draw_hand(frame, landmarks)
                    gesture = self.process_hand(landmarks, now)
                else:
                    self.previous_pinch = False
                    self.cursor.reset()

                self.draw_status(frame, gesture)

                cv2.imshow(self.config.window_name, frame)
                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break

                if key == ord("p"):
                    self.paused = not self.paused
                    self.previous_pinch = False
                    self.cursor.reset()

        finally:
            self.detector.close()
            cv2.destroyAllWindows()


def run_app():
    app = VirtualMouseApp(AppConfig())
    app.run()
