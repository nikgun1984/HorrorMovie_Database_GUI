from flask_wtf import FlaskForm
from wtforms import StringField,RadioField, SubmitField, TextAreaField,SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from wtforms import SubmitField
import pymysql

db = pymysql.connect("localhost","project","13february","horror_movies" )

class SubmissionForm(FlaskForm):
    text = TextAreaField('Query', validators=[DataRequired()])
    submit = SubmitField('Submit Query')

class EntryForm(FlaskForm):
    query = SubmitField('Generate Query')
    intQuery = SubmitField('Interesting Queries')
    forms = SubmitField('Forms')

class Form1(FlaskForm):
    choices = [('Name', 'Movie Name'),
               ('Actor', 'Actor'),
               ('Director', 'Director')]
    select = SelectField('Make your Selection', choices=choices)
    text = TextAreaField('Enter Your Search', validators=[DataRequired()])
    submit = SubmitField('Submit')

class InsertForm(FlaskForm):
    name = TextAreaField('Movie Name', validators=[DataRequired()])
    year = TextAreaField('Year', validators=[DataRequired()])
    runtime = TextAreaField('Runtime', validators=[DataRequired()])
    actor = SelectField('Select Actor')
    director = SelectField('Select Director')
    submit = SubmitField('Submit')
