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

# load teacher
@login_manager.user_loader
def load_user(teacherid):
    try:
        return models.Teacher.get(models.Teacher.id == teacherid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    g.db.close()
    return response
# //////////////////////parent //////////////////
# load parent 
@login_manager.user_loader
def load_parent(parentid):
    try:
        return models.Parent.get(models.Parent.id == parentid)
    except models.DoesNotExist:
        return None

# parent signin
def handle_signinParent(form):
    try:
        parent = models.Parent.get(models.Parent.email == form.email.data)
    except models.DoesNotExist:
        flash("parent !!!your email or password doesn't match", "error")
    else:
        if check_password_hash(parent.password, form.password.data):
            login_user(parent)
            flash('Hi parent ! You have successfully Signed In!!!', 'success signin')
            return redirect(url_for('index'))
        else:
            flash(" parent your email or password doesn't match", "error")
# /////////////////////////////////////fin parent //////////////////////////////
# signin teacher
def handle_signinTeacher(form):
    try:
        teacher = models.Teacher.get(models.Teacher.email == form.email.data)
    except models.DoesNotExist:
        flash("teacher your email or password doesn't match", "error")
    else:
        if check_password_hash(teacher.password, form.password.data):
            login_user(teacher)
            flash('Hi teacher! You have successfully Signed In!!!', 'success signin')
            return redirect(url_for('index'))
            # return render_template('aboutUs.html')
        else:
            flash("your email or password doesn't match", "error")

# landing page 
@app.route('/', methods=['GET'])
def index():
    print(current_user)
    teachersign_in_form = forms.SignInForm()
    parentsign_in_form = forms.SignInForm()
    return render_template('auth.html', teachersign_in_form=teachersign_in_form, parentsign_in_form=parentsign_in_form)
# handle logout 

@app.route('/login/parent', methods=['POST'])
def login_parent():
    parentsign_in_form = forms.SignInForm()
    if parentsign_in_form.validate_on_submit():  
        handle_signinParent(parentsign_in_form)
        return redirect(url_for('index'))

@app.route('/login/teacher', methods=['POST'])
def login_teacher():
    teachersign_in_form = forms.SignInForm()
    if teachersign_in_form.validate_on_submit():
        handle_signinTeacher(teachersign_in_form)
        return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('index'))

@app.route('/profile/<teacherid>', methods=['GET'])
def profilepage(teacherid):
    teacher = models.Teacher.get(models.Teacher.id== teacherid)
    students = models.Student.select().where(models.Student.teacher_id==int(teacher.id))
    return render_template('teacher.html', teacher=teacher,students=students) 

# parent profile
@app.route('/parentprofile/<parentid>', methods=['GET'])
def parentpage(parentid):
    parent = models.Parent.get(models.Parent.id== parentid)
    students = models.Student.select().where(models.Student.parent_id==int(parent.id))
    return render_template('parent.html', parent=parent,students=students) 

# get all students
@app.route('/students', methods =['GET'])
def students():
    students = models.Student.select().limit(100)
    return render_template('students.html', students=students)

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
            fullname= 'Brown Katia',
            address='12 west street Oakland CA',
            phonenumber='2042334343',
            biography='I have 5 years experience',
            profileImgUrl= 'https://www.opticalexpress.co.uk/images/feature-imgs/lady-with-glasses-smiling.jpg'
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
            address='44 North Street West Oakland ca',
            about='here'
            )
        models.Parent.create_parent(
            username='zola',
            email='zola@gmail.com',
            fullname ='Cherik Zola',
            password='123',
            profileImgUrl='myImage',
            phonenumber='510900667754',
            address='122 west Oakland ca',
            about='sweet'
            )
        models.Student.create_student(
            teacher=1,
            parent=1,
            fullname='Bouz Yanni',
            gender='male',
            dateOfBirth='03-04-2013',
            profileImgUrl='image',
            phonenumber='9259002323',
            address='44 North Street West Oakland ca',
            medicalNeeds='Peanut allergy',
            otherDetails='OTHER STUFFS'
            )
        models.Student.create_student(
            teacher=1,
            parent=2,
            fullname='Cherik Zira',
            gender='female',
            dateOfBirth='03-04-2012',
            profileImgUrl='image',
            phonenumber='9259001111',
            address='122 west Oakland ca',
            medicalNeeds='Peanut allergy',
            otherDetails='OTHER STUFFS'
            )
        models.Student.create_student(
            teacher=2,
            parent=2,
            fullname='Cherik Fazia',
            gender='female',
            dateOfBirth='03-04-2015',
            profileImgUrl='image',
            phonenumber='9259001111',
            address='122 west Oakland ca',
            medicalNeeds='no allergies',
            otherDetails='OTHER STUFFS'
            )
    except ValueError:
        pass

    app.run(debug=DEBUG, port=PORT)