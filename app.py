from flask import Flask, request, jsonify, render_template
import mysql.connector
from config import DB_CONFIG, THRESHOLDS
from datetime import datetime

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def check_alert(sensor_type, value):
    t = THRESHOLDS.get(sensor_type, {})
    return value < t.get("min", float('-inf')) or value > t.get("max", float('inf'))

# ── Routes ──────────────────────────────────────────────

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/data", methods=["POST"])
def ingest_data():
    """Receive sensor readings from the simulator."""
    data = request.get_json()
    required = ["sensor_id", "sensor_type", "value", "unit"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    is_alert = check_alert(data["sensor_type"], float(data["value"]))

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO sensor_readings
           (sensor_id, sensor_type, value, unit, is_alert)
           VALUES (%s, %s, %s, %s, %s)""",
        (data["sensor_id"], data["sensor_type"],
         data["value"], data["unit"], is_alert)
    )
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"status": "ok", "alert": is_alert}), 201

@app.route("/api/readings")
def get_readings():
    """Return the latest N readings, optionally filtered by type."""
    sensor_type = request.args.get("type")
    limit = int(request.args.get("limit", 50))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if sensor_type:
        cursor.execute(
            """SELECT * FROM sensor_readings
               WHERE sensor_type = %s
               ORDER BY timestamp DESC LIMIT %s""",
            (sensor_type, limit)
        )
    else:
        cursor.execute(
            """SELECT * FROM sensor_readings
               ORDER BY timestamp DESC LIMIT %s""",
            (limit,)
        )

    rows = cursor.fetchall()
    cursor.close()
    db.close()

    # Convert datetime to string for JSON
    for r in rows:
        r["timestamp"] = r["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(rows)

@app.route("/api/alerts")
def get_alerts():
    """Return only alert-flagged readings."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """SELECT * FROM sensor_readings
           WHERE is_alert = TRUE
           ORDER BY timestamp DESC LIMIT 20"""
    )
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    for r in rows:
        r["timestamp"] = r["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(rows)

@app.route("/api/summary")
def get_summary():
    """Latest value per sensor type + alert counts."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """SELECT sensor_type,
                  AVG(value)  AS avg_value,
                  MIN(value)  AS min_value,
                  MAX(value)  AS max_value,
                  SUM(is_alert) AS alert_count
           FROM sensor_readings
           WHERE timestamp >= NOW() - INTERVAL 1 HOUR
           GROUP BY sensor_type"""
    )
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True, port=5000)