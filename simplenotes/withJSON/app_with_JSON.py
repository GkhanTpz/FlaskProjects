# Import necessary Flask modules and file handling libraries
from flask import Flask
from flask_wtf import CSRFProtect
from auth.routes import auth_bp
from notes.routes import notes_bp

# Create Flask application instance
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

# Activate CSRF Protect
csrf = CSRFProtect(app)

# Register authentication blueprint with the main application
app.register_blueprint(auth_bp)
# Register notes blueprint with the main application
app.register_blueprint(notes_bp)

# Run the application in debug mode if this file is executed directly
if __name__ =="__main__":
    app.run(debug=True)