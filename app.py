import json
import os
from flask import Flask, jsonify, render_template, request, send_from_directory

app = Flask(__name__, static_folder="static", template_folder="templates")
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "events.json")


@app.route("/world-map-atlas-3840x2743-16642.jpg")
def serve_map_image():
    return send_from_directory("static", "world-map-atlas-3840x2743-16642.jpg")


def load_events():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Failed to load events:", repr(e))
            return []
    return []


def save_events(events):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)


@app.route("/")
def index():
    return render_template("World Stage2.html")


@app.route("/api/events", methods=["GET"])
def get_events():
    return jsonify(load_events())


@app.route("/api/events", methods=["POST"])
def add_event():
    events = load_events()
    new_event = request.json
    events.append(new_event)
    save_events(events)
    return jsonify({"status": "success", "event": new_event})


@app.route("/api/events/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    events = load_events()
    events = [e for e in events if e["id"] != event_id]
    save_events(events)
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)