# FlaskProject

A simple and modular Flask web application built for educational and internal use. This project demonstrates fundamental web development concepts such as routing, form handling, database integration, and frontend templating using Flask and Jinja2.

## 🚀 Features

- 🧩 Modular structure with `blueprints`
- 📄 HTML templating with Jinja2
- 📥 Form handling (GET/POST)
- 💾 SQLite/MySQL backend (configurable)
- 🔐 Basic security practices (input validation, error handling)
- 🧪 Unit testing setup

## 📁 Project Structure

```bash
FlaskProject/
│
├── simplenotes/             # Main application directory (simplenotes/withSQL or simplenotes/withJSON)
│   ├── auth/                # Login/Register Operations  (users.db, users.json)
│   ├── static/              # For CSS, JS, and image assets
│   ├── templates/           # Jinja2 HTML templates
│   ├── models/              # Database model definitions (db.py)
│   ├── notes/               # Note CRUD Operations (notes.db, notes.json)
│   ├── app.py               # Main Flask application logic
├── test/                    # Experimental testing space
│   └── (test versions of app.py, early logic trials, etc.)
├── forms.py                 # (Not built yet) For future form validation logic
├── config.py                # (Not built yet) For future configuration settings
├── requirements.txt         # List of required Python packages
└── README.md                # Project documentation (this file)
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

## 🧪 Running the Application

```bash
# Set the environment variable for development
export FLASK_APP=app.py
export FLASK_ENV=development  # Enables debug mode

# Run the Flask server
flask run
```

Access the app at: http://127.0.0.1:5000

## 🛡️ Security Notes

Do not use the built-in development server for production.

Sanitize all user input.

Consider using a WSGI server like Gunicorn or uWSGI for deployment.


## 📦 Deployment (Optional)

To deploy this project on a production environment:

1. Use Gunicorn or uWSGI with Nginx


2. Connect to a production-grade SQL database (MySQL/PostgreSQL)


3. Set up .env variables and secrets


4. Enable HTTPS (e.g., Let's Encrypt)


## ✅ To-Do (Development Roadmap)

[ ] Add user authentication system (Login/Register)

[ ] Dockerize the project

[ ] Implement RESTful API endpoints

[ ] Add unit and integration tests

[ ] Integrate CI/CD with GitHub Actions

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to fork this repository and open a pull request!

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

