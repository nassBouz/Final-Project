from flask import Flask, g
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from werkzeug.utils import secure_filename
import os
import models 
import forms 
import json
# from keyNeigh import keyNeigh

from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import json


DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'myecole.secretkey'
login_manager = LoginManager()

##sets up our login for the app
login_manager.init_app(app)
login_manager.login_view = '/'

@login_manager.user_loader
def load_user(teacherid):
    try:
        return models.Teacher.get(models.Teacher.id == teacherid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

# signin teacher
def handle_signin(form):
    try:
        teacher = models.Teacher.get(models.Teacher.email == form.email.data)
    except models.DoesNotExist:
        flash("your email or password doesn't match", "error")
    else:
        if check_password_hash(teacher.password, form.password.data):
            login_user(teacher)
            flash('Hi! You have successfully Signed In!!!', 'success signin')
            return redirect(url_for('index'))
            # return render_template('aboutUs.html')
        else:
            flash("your email or password doesn't match", "error")

# landing page 
@app.route('/', methods=('GET', 'POST'))
def index():
    sign_in_form = forms.SignInForm()
    if sign_in_form.validate_on_submit():
        handle_signin(sign_in_form)

    return render_template('auth.html', sign_in_form=sign_in_form)



@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')


if __name__ == '__main__':
    models.initialize()
    try:
        models.Teacher.create_teacher(
            username='brown',
            email="brown@ga.com",
            password='123',
            fullname= 'Brown Simpson',
            address='12 west street Oakland CA',
            phonenumber='2042334343',
            biography='I have 5 years experience',
            profileImgUrl= 'http://interactive.nydailynews.com/2016/05/simpsons-quiz/img/simp1.jpg'
            )
        models.Teacher.create_teacher(
            username='Jeff',
            email="jeff@ga.com",
            password='123',
            fullname= 'Jeff Habib',
            address='23 west street Oakland CA',
            phonenumber='212334390008',
            biography='I have 2 years experience working with kids',
            profileImgUrl= 'http://interactive.nydailynews.com/2016/05/simpsons-quiz/img/simp1.jpg'
            )
        models.Parent.create_parent(
            username='nassBouz',
            email='bouzianenassima@gmail.com',
            fullname ='Nassima Bouz ',
            password='123',
            profileImgUrl='myImage',
            phonenumber='51090095454',
            address='122 west Oakland ca',
            about='here'
            )
        models.Parent.create_parent(
            username='zola',
            email='zola@gmail.com',
            fullname ='Zola Cherik',
            password='123',
            profileImgUrl='myImage',
            phonenumber='510900667754',
            address='122 west Oakland ca',
            about='sweet'
            )
        models.Student.create_student(
            teacher=1,
            parent=1,
            fullname='Boulou Tarik',
            gender='male',
            dateOfBirth='03-04-2012',
            profileImgUrl='image',
            phonenumber='9259002323',
            address='122 west Oakland ca',
            medicalNeeds='Peanut allergy'
            )
    except ValueError:
        pass

    app.run(debug=DEBUG, port=PORT)