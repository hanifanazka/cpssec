from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_logs():
    conn = sqlite3.connect("medical_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 20")
    logs = cursor.fetchall()
    conn.close()
    return logs

@app.route("/")
def home():
    logs = get_logs()
    return render_template("index.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)

