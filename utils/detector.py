"""
YOLO-based human detection — loads model once and exposes a detect() function.
"""
import cv2
import numpy as np
from ultralytics import YOLO
from config import Config

# Load model once at startup
_model = YOLO(Config.MODEL_PATH)


def detect_humans(frame: np.ndarray) -> tuple[np.ndarray, bool]:
    """
    Run YOLOv8 inference on a frame.
    Draws bounding boxes on detected persons.
    Returns (annotated_frame, person_detected).
    """
    results = _model(frame)
    person_found = False
    annotated = frame.copy()

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            name = _model.names[cls]
            conf = float(box.conf[0])

            if name == "person":
                person_found = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Bounding box
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 80), 3)

                # Label background
                label = f"PERSON  {conf:.0%}"
                (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 2)
                cv2.rectangle(annotated, (x1, y1 - lh - 12), (x1 + lw + 8, y1), (0, 255, 80), -1)

                # Label text
                cv2.putText(
                    annotated, label,
                    (x1 + 4, y1 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (0, 0, 0), 2
                )

    return annotated, person_found
