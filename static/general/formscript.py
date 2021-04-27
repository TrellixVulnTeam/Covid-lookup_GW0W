from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    searchquery = StringField('Enter Your Country:')
    submit = SubmitField('Search')