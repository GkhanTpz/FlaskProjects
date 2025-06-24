from flask import Flask

app = Flask(__name__)  # Flask uygulaması başlatılıyor

@app.route("/")        # Ana sayfa adresi (localhost:5000 gibi)
def home():
    return "Merhaba Gökhan!"  # Tarayıcıda gösterilecek yazı

if __name__ == "__main__":
    app.run(debug=True)  # Uygulama başlatılır
