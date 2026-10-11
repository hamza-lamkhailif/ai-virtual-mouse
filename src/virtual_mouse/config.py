from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class AppConfig:
    camera_index: int = 0
    frame_width: int = 1280
    frame_height: int = 720

    smoothing: float = 0.25
    margin: float = 0.10
    pinch_threshold: float = 0.045
    click_cooldown: float = 0.35

    detection_confidence: float = 0.6
    presence_confidence: float = 0.6
    tracking_confidence: float = 0.6
    max_hands: int = 1

    window_name: str = "AI Virtual Mouse"
    model_path: Path = (
        PROJECT_ROOT / "assets" / "hand_landmarker.task"
    )
