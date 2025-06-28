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
    
notes = load_notes()        # notları burada tutacağız

app = Flask(__name__)       # Flask uygulaması başlatılıyor
@app.route("/", methods=["GET", "POST"])        # Ana sayfa adresi (localhost:5000 gibi)
def home():
    if request.method == "POST":
        note = request.form.get("note")         #Formdan gelen notu al
        if note:        # Boş değilse listeye ekle
            notes.append(note)      # formdan gelen metni notes listesine ekler
            save_notes(notes)       # Her eklemeden sonra JSON'a yaz
    return render_template("index.html", notes=notes)       # Tarayıcıda gösterilecek html dosyası

@app.route("/delete", methods=["POST"])
def delete_note():
    index = int(request.form.get("index"))
    if 0 <= index < len(notes):  # Güvenlik kontrolü
        del notes[index]         # Listeden sil
        save_notes(notes)        # JSON dosyasını güncelle
    return redirect("/")         # Sayfayı yenile (anasayfa)

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_note(index):
    if request.method == "POST":
        new_note = request.form.get("note")
        if new_note:
            notes[index] = new_note
            save_notes(notes)
        return redirect("/")
    current_note = notes[index]
    return render_template("edit.html", note=current_note, index=index)

if __name__ == "__main__":
    app.run(debug=True)         # Uygulama başlatılır
