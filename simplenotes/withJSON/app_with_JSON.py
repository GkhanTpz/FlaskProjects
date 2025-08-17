# Import necessary Flask modules and file handling libraries
from flask import Flask, render_template
from flask_wtf import CSRFProtect
from auth.routes import auth_bp
from notes.routes import notes_bp

# Create Flask application instance
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

# Enable CSRF protection for security
csrf = CSRFProtect(app)

# Register authentication blueprint with the main application
app.register_blueprint(auth_bp)
# Register notes blueprint with the main application
app.register_blueprint(notes_bp)

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 page not found errors"""
    return render_template("errors/404.html"), 404
    
@app.errorhandler(500)
def internal_error(error):
    """Handle 500 internal server errors"""
    return render_template("errors/500.html"), 500
    
# Run the application in debug mode if this file is executed directly
if __name__ =="__main__":
    app.run(debug=False)