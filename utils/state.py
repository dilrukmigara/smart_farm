"""
Shared detection state — single source of truth for the latest frame data.
"""
from datetime import datetime

class DetectionState:
    def __init__(self):
        self.original = ""
        self.result = ""
        self.status = "Waiting for camera..."
        self.person_detected = False
        self.motion_detected = False
        self.motion_source = ""
        self.last_event = ""
        self.last_updated = None
        self.detection_count = 0
        self.total_frames = 0
        self.last_alert_time = None

    def update(self, original, result, person):
        self.original = original
        self.result = result
        self.person_detected = person
        self.motion_detected = False
        self.motion_source = ""
        self.last_event = ""
        self.status = "🚨 Human Detected!" if person else "✅ No Human Detected"
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total_frames += 1
        if person:
            self.detection_count += 1

    def update_motion(self, source: str, details: str):
        self.motion_detected = True
        self.motion_source = source
        self.last_event = details
        self.status = f"🚨 Motion detected by {source}"
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "original": self.original,
            "result": self.result,
            "status": self.status,
            "person_detected": self.person_detected,
            "motion_detected": self.motion_detected,
            "motion_source": self.motion_source,
            "last_event": self.last_event,
            "last_updated": self.last_updated,
            "detection_count": self.detection_count,
            "total_frames": self.total_frames,
        }

# Global singleton
state = DetectionState()
