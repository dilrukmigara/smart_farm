from flask import Flask, render_template, send_from_directory, jsonify
from routes.upload import upload_bp
from routes.stream import stream_bp
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
