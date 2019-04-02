from flask_wtf import FlaskForm as Form 
from models import Teacher
from models import Parent
from models import Student
from wtforms import StringField, PasswordField, TextAreaField, TextField, SubmitField, IntegerField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo)

def name_exists(form, field):
    if Teacher.select().where(Teacher.username == field.data).exists():
        raise ValidationError('Teacher with that name already exists.')

class SignInForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class StudentEditForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Regexp( r'^[a-zA-Z0-9_]+$', message=("Username should be one word, letters, numbers, and underscores only.")),name_exists])
    fullname= StringField('Full Name',validators=[ DataRequired(), Length(min=2)])
    profileImgUrl = StringField("Image")

# class CreateMessageForm(form):
# class EditMessageForm(Form):
# class EditStudentLevel(Form):
# class EditStudentMedicalRecord(Form):



