from flask import Flask, render_template, send_from_directory, jsonify, request
from routes.upload import upload_bp
from routes.stream import stream_bp
from config import Config
from db import db
from models import SensorData
from utils.state import state
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Register blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(stream_bp)

# Serve saved images
@app.route('/photos/<filename>')
def serve_photo(filename):
    return send_from_directory(Config.SAVE_FOLDER, filename)

@app.route('/results/<filename>')
def serve_result(filename):
    return send_from_directory(Config.RESULT_FOLDER, filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sensors')
def sensors():

    rain_raw = request.args.get('rain')
    soil_raw = request.args.get('soil')
    temp_raw = request.args.get('temp')
    hum_raw = request.args.get('hum')

    try:
        rain = int(rain_raw) if rain_raw is not None else None
    except ValueError:
        rain = None

    try:
        soil = int(soil_raw) if soil_raw is not None else None
    except ValueError:
        soil = None

    try:
        temperature = float(temp_raw) if temp_raw is not None else None
    except ValueError:
        temperature = None

    try:
        humidity = float(hum_raw) if hum_raw is not None else None
    except ValueError:
        humidity = None

    print("========== SENSOR DATA ==========")
    print("Rain:", rain)
    print("Soil:", soil)
    print("Temperature:", temperature)
    print("Humidity:", humidity)

    data = SensorData(
        rain=rain,
        soil=soil,
        temperature=temperature,
        humidity=humidity
    )
    db.session.add(data)
    db.session.commit()

    state.update_sensors(rain, soil, temperature, humidity)

    return jsonify({
        "message": "Sensor data saved",
        "sensors": {
            "rain": rain,
            "soil": soil,
            "temperature": temperature,
            "humidity": humidity
        }
    })

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)

from models import SensorData

with app.app_context():
    db.create_all()
