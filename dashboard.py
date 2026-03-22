from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

LOG_FILE = "logs/attack_log.csv"

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    if not os.path.exists(LOG_FILE):
        return jsonify({"attacks": 0, "data": []})

    df = pd.read_csv(LOG_FILE)

    if df.empty:
        return jsonify({"attacks": 0, "data": []})

    # Count only real attacks (not BENIGN)
    attack_df = df[df["Attack Type"] != "BENIGN"]

    return jsonify({
        "attacks": len(attack_df),
        "data": attack_df.to_dict(orient="records")
    })

if __name__ == "__main__":
    app.run(debug=True)
