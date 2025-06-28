from flask import Flask, render_template, request, redirect
import json
import os

DATA_FILE = "notes.json"

def save_notes(notes):
   # Save notes to JSON file
   with open(DATA_FILE, "w", encoding="utf-8") as f:
       json.dump(notes, f, ensure_ascii=False, indent=4)

def load_notes():
   # Load notes from JSON file if exists
   if os.path.exists(DATA_FILE):
       with open(DATA_FILE, "r", encoding="utf-8") as f:
           return json.load(f)
   return []
   
notes = load_notes()        # we will store notes here

app = Flask(__name__)       # Flask application is starting

@app.route("/", methods=["GET", "POST"])        # Main page address (like localhost:5000)
def home():
   # Handle form submission
   if request.method == "POST":
       note = request.form.get("note")         # Get the note from the form
       if note:        # If not empty, add to list
           notes.append(note)      # adds the text from form to notes list
           save_notes(notes)       # Write to JSON after each addition
   return render_template("index.html", notes=notes)       # HTML file to be displayed in browser

@app.route("/delete", methods=["POST"])
def delete_note():
   # Get index and delete note
   index = int(request.form.get("index"))
   if 0 <= index < len(notes):  # Security check
       del notes[index]         # Delete from list
       save_notes(notes)        # Update JSON file
   return redirect("/")         # Refresh page (homepage)

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_note(index):
   # Handle note editing
   if request.method == "POST":
       new_note = request.form.get("note")
       if new_note:
           notes[index] = new_note  # Update note
           save_notes(notes)        # Save changes
       return redirect("/")
   current_note = notes[index]      # Get current note for editing
   return render_template("edit.html", note=current_note, index=index)

if __name__ == "__main__":
   app.run(debug=True)         # Application is started
