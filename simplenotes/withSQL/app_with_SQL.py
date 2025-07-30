# Import necessary Flask modules and database functions
from flask import Flask
from auth.routes import auth
from notes.routes import notes_bp
from flask_wtf.csrf import CSRFProtect

# Create Flask application instance
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

# Activate CSRF Protect
csrf = CSRFProtect(app)

app.register_blueprint(auth)
app.register_blueprint(notes_bp)

# Run the application in debug mode if this file is executed directly
if __name__ =="__main__":
    app.run(debug=True)