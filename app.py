from flask import Flask, request, render_template, send_file, redirect, url_for
import sqlite3, json, os
from werkzeug.utils import secure_filename
from pathlib import Path

app = Flask(__name__)
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)
DB_PATH = UPLOAD_FOLDER / "copilot_metrics.db"

def create_db(json_data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS completions")
    cur.execute("DROP TABLE IF EXISTS summary")

    cur.execute("""
        CREATE TABLE completions (
            date TEXT,
            editor TEXT,
            language TEXT,
            code_suggestions INTEGER,
            code_acceptances INTEGER,
            code_lines_suggested INTEGER,
            code_lines_accepted INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE summary (
            date TEXT PRIMARY KEY,
            total_active_users INTEGER,
            total_engaged_users INTEGER
        )
    """)

    for entry in json_data:
        date = entry["date"]
        cur.execute("INSERT INTO summary VALUES (?, ?, ?)", (
            date,
            entry.get("total_active_users", 0),
            entry.get("total_engaged_users", 0)
        ))

        completions = entry.get("copilot_ide_code_completions", {})
        for editor in completions.get("editors", []):
            editor_name = editor["name"]
            for model in editor.get("models", []):
                for lang in model.get("languages", []):
                    cur.execute("""
                        INSERT INTO completions VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        date,
                        editor_name,
                        lang.get("name", "unknown"),
                        lang.get("total_code_suggestions", 0),
                        lang.get("total_code_acceptances", 0),
                        lang.get("total_code_lines_suggested", 0),
                        lang.get("total_code_lines_accepted", 0)
                    ))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".json"):
            filepath = UPLOAD_FOLDER / secure_filename(file.filename)
            file.save(filepath)
            with open(filepath) as f:
                data = json.load(f)
                create_db(data)
            return redirect(url_for("download"))
        else:
            return "Invalid file type. Please upload a .json file."
    return render_template("upload.html")

@app.route("/download")
def download():
    return send_file(DB_PATH, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
