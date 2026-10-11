class CursorController:
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        smoothing: float = 0.25,
        margin: float = 0.10,
    ):
        if not 0 < smoothing <= 1:
            raise ValueError("Smoothing must be in (0, 1].")

        if not 0 <= margin < 0.5:
            raise ValueError("Margin must be in [0, 0.5).")

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothing = smoothing
        self.margin = margin

        self.x = None
        self.y = None

    def map_coordinates(self, x: float, y: float):
        x = (x - self.margin) / (1 - 2 * self.margin)
        y = (y - self.margin) / (1 - 2 * self.margin)

        x = max(0.0, min(1.0, x))
        y = max(0.0, min(1.0, y))

        return (
            round(x * (self.screen_width - 1)),
            round(y * (self.screen_height - 1)),
        )

    def update(self, x: float, y: float):
        target_x, target_y = self.map_coordinates(x, y)

        if self.x is None:
            self.x = float(target_x)
            self.y = float(target_y)
        else:
            self.x += self.smoothing * (target_x - self.x)
            self.y += self.smoothing * (target_y - self.y)

        return round(self.x), round(self.y)

    def reset(self):
        self.x = None
        self.y = None
