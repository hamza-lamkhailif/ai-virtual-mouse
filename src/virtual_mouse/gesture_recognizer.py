import math


class GestureRecognizer:
    def __init__(self, pinch_threshold: float):
        self.pinch_threshold = pinch_threshold

    @staticmethod
    def distance(point_a, point_b) -> float:
        return math.hypot(
            point_a.x - point_b.x,
            point_a.y - point_b.y,
        )

    def is_pinching(self, landmarks) -> bool:
        # Landmark 4: thumb tip
        # Landmark 8: index finger tip
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        return (
            self.distance(thumb_tip, index_tip)
            < self.pinch_threshold
        )
