from flask import Flask, render_template, request, redirect, url_for
from test_db import init_db, get_notes, update_note_in_db, insert_note, delete_note_from_db

app = Flask(__name__)
init_db()

@app.route("/")
def home():
   notes = get_notes()
   return render_template("test_index_with_SQL.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    text = request.form.get("note")
    if text:
        insert_note(text)
    return redirect(url_for("home"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete_note(id):
    delete_note_from_db(id)
    return redirect(url_for("home"))

@app.route("/edit/<int:id>")
def edit_note(id):
    notes = get_notes()
    current_note = next((note for note in notes if note[0] == id), None)

    if current_note is None:
        return "Note not found", 404
    return render_template("test_edit_with_SQL.html", note=current_note)

@app.route("/update/<int:id>", methods=["POST"])
def update_note(id):
    new_text = request.form.get("new_note")
    update_note_in_db(id, new_text)
    return redirect(url_for("home"))

if __name__ =="__main__":
    app.run(debug=True)