from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=255)])
    submit = SubmitField('Add User')

class UpdateUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=255)])
    submit = SubmitField('Update User')
