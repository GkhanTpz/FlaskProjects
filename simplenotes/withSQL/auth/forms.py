"""Forms.py shared between JSON & SQL backends."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, length


class LoginForm(FlaskForm):
    """Form for user login with username and password fields"""
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])    # Username field with minimum 3 characters
    password = PasswordField("Password", validators=[DataRequired()])                  # Password field (required)
    submit = SubmitField("Login")                                                     # Submit button for login

class RegisterForm(FlaskForm):
    """Form for user registration with validation"""
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])    # Username field with minimum 3 characters
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])  # Password field with minimum 4 characters
    confirm_password = PasswordField("Confirm Password", validators=[               # Password confirmation field
        DataRequired(), EqualTo("password", message="Passwords must match!")
    ])
    submit = SubmitField("Register")                                                  # Submit button for registration