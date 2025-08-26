from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NoteForm(FlaskForm):
    """Form for creating and editing notes"""
    note = StringField("Notes",validators=[DataRequired(), Length(max=150)])
    submit = SubmitField("Save")

class SearchForm(FlaskForm):
    """Form for searching notes"""
    query = StringField("Search", validators=[DataRequired(), Length(max=150)])
    submit = SubmitField("Search")
    
    class Meta:
        csrf = False