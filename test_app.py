from flask import Flask, render_template, request
import json
import os

DATA_FILE = "notes.json"

def save_notes(notes):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)
        
def load_notes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

notes = load_notes()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if note:
            notes.append(note)
            save_notes(notes)
    return render_template("test_index.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)