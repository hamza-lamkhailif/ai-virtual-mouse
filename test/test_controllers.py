from types import SimpleNamespace

from virtual_mouse.cursor_controller import CursorController
from virtual_mouse.gesture_recognizer import GestureRecognizer


def test_cursor_maps_center_to_center():
    cursor = CursorController(
        screen_width=1920,
        screen_height=1080,
        smoothing=1.0,
        margin=0.1,
    )

    x, y = cursor.update(0.5, 0.5)

    assert x == 960
    assert y == 540


def test_cursor_clamps_to_screen():
    cursor = CursorController(
        screen_width=1920,
        screen_height=1080,
        smoothing=1.0,
        margin=0.1,
    )

    x, y = cursor.update(2.0, -1.0)

    assert 0 <= x < 1920
    assert 0 <= y < 1080


def test_cursor_reset():
    cursor = CursorController(
        screen_width=1920,
        screen_height=1080,
    )

    cursor.update(0.5, 0.5)
    cursor.reset()

    assert cursor.x is None
    assert cursor.y is None


def test_pinch_is_detected():
    recognizer = GestureRecognizer(0.045)

    landmarks = [
        SimpleNamespace(x=0.5, y=0.5)
        for _ in range(21)
    ]

    landmarks[4] = SimpleNamespace(x=0.500, y=0.500)
    landmarks[8] = SimpleNamespace(x=0.510, y=0.510)

    assert recognizer.is_pinching(landmarks)


def test_pinch_is_not_detected():
    recognizer = GestureRecognizer(0.045)

    landmarks = [
        SimpleNamespace(x=0.5, y=0.5)
        for _ in range(21)
    ]

    landmarks[4] = SimpleNamespace(x=0.2, y=0.2)
    landmarks[8] = SimpleNamespace(x=0.5, y=0.5)

    assert not recognizer.is_pinching(landmarks)
