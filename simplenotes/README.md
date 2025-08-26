# 🐍 Simple Notes with Flask

A simple and modular Flask web application built for educational and internal use. This project demonstrates fundamental web development concepts such as routing, form handling, database integration, and frontend templating using Flask and Jinja2.

---

## 🚀 Features

- 🧩 Modular structure with Blueprints (`auth/`, `notes/`, `models/`)
- 📄 Jinja2 templating system for dynamic HTML
- 📥 Form handling with GET and POST methods
- 💾 Dual backend logic (JSON and SQLite)
- 🧰 Session-based login/logout/register system
- 💡 Flash messages for user feedback
- 🎨 Bootstrap-powered responsive UI
- 🧪 Testing-ready (unit testing planned)
- 🔐 Basic security practices (input validation, login protection)

---

## 📁 Project Structure

```bash
FlaskProject/
│
├── simplenotes/          # Including withJSON and withSQL (simplenotes/withJSON or simplenotes/SQL)
│   ├── auth/             # Login/Register logic (SQLite or JSON)
│   ├── notes/            # Note CRUD (SQLite or JSON)
│   ├── models/           # SQLite database logic (db.py)
│   ├── static/           # Custom CSS or image files
│   ├── templates/        # Jinja2 templates with index.html structure
│   ├── app.py            # Main application file
│
├── test/                 # Experimental testing & drafts
├── config.py             # (Planned) App config (e.g., database URI)
├── requirements.txt      # Python dependency list
└── README.md             # Project documentation (this file)
```

## ⚙️ Installation

> Requires Python 3.8+

```bash
# Clone the repo
git clone https://github.com/yourusername/FlaskProject.git
cd FlaskProject

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🧪 Running the Application

```bash
# Set the environment variable for development
export FLASK_APP=app.py
export FLASK_ENV=development  # Enables debug mode

# Run the Flask server
flask run
```

Access the app at: http://127.0.0.1:5000

---

## 🛡️ Security Notes

Do not use the built-in development server for production.

Sanitize all user input.

Consider using a WSGI server like Gunicorn or uWSGI for deployment.

---

## 📦 Deployment (Optional)

To deploy on a production environment:
1. Use a WSGI server like Gunicorn or uWSGI  
2. Switch to a production-grade SQL database (MySQL/PostgreSQL)  
3. Store secrets in environment variables or .env files  
4. Set up HTTPS (via Let’s Encrypt)  
5. Reverse proxy with Nginx or Apache  

---

## 🛡️ Security Notes
	•	Never use the built-in Flask server in production
	•	Sanitize all user inputs
	•	Protect routes using @login_required
	•	Avoid exposing secrets or raw database queries

---

## ✅ Development Roadmap (To-Do)
	•	Implement user login/register with session support
	•	JSON-based CRUD for notes
	•	SQLite-based CRUD for notes
	•	Modularize with Flask Blueprints
	•	Bootstrap layout implementation
	•	Add flash messages with Bootstrap alerts
	•	Restrict notes per user (session-based filtering)
	•	Create RESTful API endpoints for notes
	•	Add unit and integration tests
	•	Create per-module README files
	•	Dockerize the project
	•	Set up GitHub Actions for CI/CD

---

## 🤝 Contributing

Contributions, issues, and suggestions are always welcome.
Feel free to fork this repository and open a pull request!

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
