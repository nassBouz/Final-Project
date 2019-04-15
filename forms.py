from flask_wtf import FlaskForm as Form 
from models import User
from models import Student
from models import Message
from wtforms import StringField, PasswordField, TextAreaField, TextField, SubmitField, IntegerField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo)

def name_exists(form, field):
    if Teacher.select().where(User.username == field.data).exists():
        raise ValidationError('Teacher with that name already exists.')

class SignInForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class MessageForm(Form):
    text = TextAreaField("Content", validators=[DataRequired()])
    title = TextField("Title",  validators=[DataRequired()])
    imageUrl = TextAreaField("image here", default="noImage")
    imageFile = TextAreaField("image file here")
    submit = SubmitField('Create Message')

class UserEditForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Regexp( r'^[a-zA-Z0-9_]+$', message=("Username should be one word, letters, numbers, and underscores only.")),name_exists])
    fullname= StringField('Full Name',validators=[ DataRequired(), Length(min=2)])
    profileImgUrl = StringField("Image")

class EditStudent(Form):
    medicalNeedds = TextAreaField("medical needs",  validators=[DataRequired()])
    fullname = StringField('Full Name',validators=[ DataRequired(), Length(min=2)])
    studentLevel= IntegerField(default=0)
    workingOn = TextAreaField()
    phonenumber = IntegerField()

class EditStudentParent(Form):
    medicalNeeds = TextAreaField("medical needs",  validators=[DataRequired()])
    phonenumber = IntegerField()




