from flask import Flask, render_template, request, redirect
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
    return render_template("test_index_with_JSON.html", notes=notes)

@app.route("/delete", methods=["POST"])
def delete_note():
    index = int(request.form.get("index"))
    if 0 <= index < len(notes):
        del notes[index]
        save_notes(notes)
    return redirect("/")

@app.route("/test_edit_with_JSON/<int:index>", methods=["GET", "POST"])
def edit_note(index):
    if request.method == "POST":
        new_note = request.form.get("note")
        if new_note:
            notes[index] = new_note
            save_notes(notes)
        return redirect("/")
    current_note = notes[index]
    return render_template("test_edit_with_JSON.html", note=current_note, index=index)

if __name__ =="__main__":
    app.run(debug=True)