from db import db
from datetime import datetime

class SensorData(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    rain = db.Column(db.Integer)

    soil = db.Column(db.Integer)

    temperature = db.Column(db.Float)

    humidity = db.Column(db.Float)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )