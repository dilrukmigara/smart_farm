"""
/upload — receives raw JPEG bytes from ESP32-CAM,
runs detection, updates shared state, fires Telegram alert.
"""

import cv2
import numpy as np
from flask import Blueprint, request, jsonify
from datetime import datetime
from config import Config
from utils.state import state
from utils.detector import detect_humans
from utils.telegram import (
    send_telegram_alert,
    send_telegram_message
)

upload_bp = Blueprint("upload", __name__)


# create trigger variable inside state
if not hasattr(state, "motion_trigger"):
    state.motion_trigger = False


# ============================================
# Upload endpoint
# ============================================
@upload_bp.route("/upload", methods=["POST"])
def upload():

    raw = request.data

    if not raw:
        return "No data",400

    nparr=np.frombuffer(
        raw,
        np.uint8
    )

    frame=cv2.imdecode(
        nparr,
        cv2.IMREAD_COLOR
    )

    if frame is None:
        return "Image decode failed",400


    filename=datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    original_path=(
        f"{Config.SAVE_FOLDER}/{filename}.jpg"
    )

    cv2.imwrite(
        original_path,
        frame
    )


    annotated,person=detect_humans(frame)


    result_path=(
        f"{Config.RESULT_FOLDER}/{filename}.jpg"
    )

    cv2.imwrite(
        result_path,
        annotated
    )


    state.update(
        original_path,
        result_path,
        person
    )


    if person:

        send_telegram_alert(
            result_path
        )


    return "ok",200



# ============================================
# Motion endpoint
# ESP32 PIR eka mekata POST karanawa
# ============================================
# ============================================
# Motion endpoint
# ============================================
@upload_bp.route("/motion", methods=["GET","POST"])
def motion():

    # GET request support
    if request.method=="GET":

        sensor=request.args.get(
            "sensor",
            "ESP32"
        )

        details=(
            f"Motion from {sensor}"
        )

        state.update_motion(
            sensor,
            details
        )

        send_telegram_message(
            f"🚨 *MOTION DETECTED* 🚨\n\n{details}"
        )

        state.motion_trigger=True

        print("Motion ON")

        return "OK",200


    # POST JSON support
    data=request.get_json(
        silent=True
    )

    if data is None:

        return jsonify({
            "error":"invalid json"
        }),400


    source=data.get(
        "source",
        "ESP32"
    )

    details=(
        f"Motion event from {source}"
    )

    state.update_motion(
        source,
        details
    )

    send_telegram_message(
        f"🚨 *MOTION DETECTED* 🚨\n\n{details}"
    )

    state.motion_trigger=True

    print("Motion ON")

    return "OK",200

# ============================================
# ESP32 CAM checks this
# ============================================
@upload_bp.route("/check", methods=["GET"])
def check():

    print(
      "ESP asked:",
      state.motion_trigger
    )

    if state.motion_trigger:

        state.motion_trigger=False

        print(
          "YES sent"
        )

        return "YES",200


    return "NO",200