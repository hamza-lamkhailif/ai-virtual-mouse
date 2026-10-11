import time

import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, config):
        if not config.model_path.is_file():
            raise FileNotFoundError(
                f"Hand model not found: {config.model_path}"
            )

        self.config = config
        self.vision = mp.tasks.vision

        options = self.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(
                model_asset_path=str(config.model_path)
            ),
            running_mode=self.vision.RunningMode.VIDEO,
            num_hands=config.max_hands,
            min_hand_detection_confidence=(
                config.detection_confidence
            ),
            min_hand_presence_confidence=(
                config.presence_confidence
            ),
            min_tracking_confidence=(
                config.tracking_confidence
            ),
        )

        self.landmarker = (
            self.vision.HandLandmarker.create_from_options(
                options
            )
        )

        self.camera = cv2.VideoCapture(config.camera_index)

        if not self.camera.isOpened():
            self.landmarker.close()
            raise RuntimeError("Could not open webcam.")

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH, config.frame_width
        )
        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT, config.frame_height
        )

        self.last_timestamp_ms = -1

    def read_frame(self):
        success, frame = self.camera.read()

        if not success:
            return None, []

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb,
        )

        # VIDEO mode requires strictly increasing timestamps.
        timestamp_ms = time.monotonic_ns() // 1_000_000
        timestamp_ms = max(
            timestamp_ms, self.last_timestamp_ms + 1
        )
        self.last_timestamp_ms = timestamp_ms

        result = self.landmarker.detect_for_video(
            image, timestamp_ms
        )

        hands = result.hand_landmarks or []
        return frame, hands

    def close(self):
        self.camera.release()
        self.landmarker.close()
