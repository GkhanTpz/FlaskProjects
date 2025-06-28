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
    
notes = load_notes() # notları burada tutacağız

app = Flask(__name__)  # Flask uygulaması başlatılıyor

@app.route("/", methods=["GET", "POST"])        # Ana sayfa adresi (localhost:5000 gibi)
def home():
    if request.method == "POST":
        note = request.form.get("note") #Formdan gelen notu al
        if note: # Boş değilse listeye ekle
            notes.append(note) # formdan gelen metni notes listesine ekler
            save_notes(notes) # Her eklemeden sonra JSON'a yaz
    return render_template("index.html", notes=notes)  # Tarayıcıda gösterilecek html dosyası

if __name__ == "__main__":
    app.run(debug=True)  # Uygulama başlatılır
