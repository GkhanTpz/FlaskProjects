from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NoteForm(FlaskForm):
    note = StringField("Notes",validators=[DataRequired(), Length(max=150)])
    submit = SubmitField("Save")

class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired(), Length(max=150)])
    submit = SubmitField("Search")