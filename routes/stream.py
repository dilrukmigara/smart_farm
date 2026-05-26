"""
/status  — returns latest detection state as JSON (polled by frontend JS).
/history — returns recent detection log.
"""
from flask import Blueprint, jsonify
from utils.state import state

stream_bp = Blueprint("stream", __name__)


@stream_bp.route("/status")
def status():
    return jsonify(state.to_dict())
