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
# for mail alert
from flask_mail import Mail, Message
from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import json



DEBUG = True
PORT = 8000

app = Flask(__name__,instance_relative_config=True)


# //////////// mail setup/////////////
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bouznass19@gmail.com'
app.config['MAIL_PASSWORD'] = 'Afroukh99'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.secret_key = 'myecole.secretkey'
login_manager = LoginManager()

##sets up our login for the app
login_manager.init_app(app)
login_manager.login_view = '/'


# load teacher
@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
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

# signin teacher
def handle_signin(form):
    try:
        print(form.email.data)
        user = models.User.get(models.User.email == form.email.data)
    except models.DoesNotExist:
        flash("teacher your email or password doesn't match", "error")
    else:
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Hi teacher! You have successfully Signed In!!!', 'success signin')
            return redirect(url_for('index'))
            # return render_template('aboutUs.html')
        else:
            flash("your email or password doesn't match", "error")

# landing page 
@app.route('/', methods=['GET', 'POST'])
def index():
    print(current_user)
    sign_in_form = forms.SignInForm()
    if sign_in_form.validate_on_submit():
        handle_signin(sign_in_form)
        return redirect(url_for('index'))
    return render_template('auth.html', sign_in_form=sign_in_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('index'))

@app.route('/teacherprofile/<userid>', methods=['GET'])
def profilepage(userid):
    user = models.User.get(models.User.id == int(userid))
    students = models.Student.select().where(models.Student.teacher_id==int(user.id))
    return render_template('teacher.html', user=user ,students=students) 

@app.route('/parentprofile/<userid>', methods=['GET'])
def parentpage(userid):
    user = models.User.get(models.User.id == int(userid))
    students = models.Student.select().where(models.Student.parent_id==int(user.id))
    return render_template('parent.html', user=user,students=students)




@app.route('/message/<studentid>', methods =['GET', 'POST','PUT'])
def getstudent(studentid=None):
    if studentid != None :
        student = models.Student.select().where(models.Student.id == int(studentid)).get()
        user = g.user._get_current_object()
        messages = models.Message.select().where(models.Message.student_id==int(studentid))
        form = forms.MessageForm()
        senderEmail ='bouznass19@gmail.com'
        receiverEmail = 'bouznass19@gmail.com'
        if form.validate_on_submit():
            if user.role == 'teacher':
                models.Message.create(
                    sender= user.id,
                    recipient = student.parent,
                    title= form.title.data,
                    text= form.text.data,
                    imageFile=form.imageFile.data,
                    imageUrl=form.imageUrl.data,
                    student=student
                )
                msg = Message("Good Morning , your pyou have a new message",sender=senderEmail,recipients=[receiverEmail])
                msg.body = f'Hello {student.parent.fullname}, {user.fullname} has sent you this message : {form.text.data}'
                mail.send(msg)
                return redirect("/message/{}".format(studentid))
                # return render_template('student.html',form=form ,student=student, user=user, messages=messages)
            else:
                models.Message.create(
                    sender= user.id,
                    recipient = student.teacher,
                    title= form.title.data,
                    text= form.text.data,
                    imageFile=form.imageFile.data,
                    imageUrl=form.imageUrl.data,
                    student=student
                )
                msg = Message("Good Morning , your have a new message from ",sender=senderEmail,recipients=[receiverEmail])
                msg.body = f'Hello {student.parent.fullname}, {user.fullname} has sent you this message : {form.text.data}'
                mail.send(msg)
                # return render_template('student.html',form=form ,student=student, user=user, messages=messages)
                return redirect("/message/{}".format(studentid))

        return render_template('student.html',form=form ,student=student, user=user, messages=messages)

#edit student informations
# @app.route('/edit-student/<studentid>', methods=['GET','POST'])
# def edit_student(studentid=None):
#     student = models.Student.select().where(models.Student.id == int(studentid)).get()
#     form = forms.EditStudent()
    
#     if current_user.role =='parent'
#         if form.validate_on_submit():
#             student.medicalNeeds = form.medicalNeeds.data
#             flash('Your chnges have been saved', 'succes')
#             return render_template('student.html', form=form,student=student)
    
#     return render_template('student.html', form=form,student=student)






# edit message
@app.route('/edit-message/<messageid>', methods=['GET','POST'])
def edit_message(messageid=None):
    print(messageid)
    message_id = int(messageid)
    message = models.Message.get(models.Message.id == message_id)
    studentid = message.student_id
    print('there is the student id in edit:', studentid)
    student = models.Student.get_by_id(int(studentid))
    user = g.user._get_current_object()
    form = forms.MessageForm()
    if form.validate_on_submit():
        print('form valid')
        message.title= form.title.data
        message.text= form.text.data
        message.imageFile=form.imageFile.data
        message.imageUrl=form.imageUrl.data
        message.save()
        flash('Your changes have been saved.', 'success')
        # return redirect("/message/{}".format(studentid))
        # return redirect(url_for('message', messageid= message.id,form=form))
        return render_template('student.html',form=form ,student=student,user=user, message=message)
    if message != None:
        print('message')
        print(message.title)
        form.title.data = message.title
        form.text.data = message.text
        form.imageFile.data = message.imageFile
        form.imageUrl.data = message.imageUrl
        # form.sender.data = message.sender
        # form.recipient.data = message.recipient
    
    return render_template('student.html',form=form ,student=student,user=user, message=message)
    

# delete message
@app.route('/message/<messageid>/delete')
def delete_message(messageid):
    message_id = int(messageid)
    message = models.Message.get(models.Message.id == message_id)
    studentid = message.student_id
    message.delete_instance()

    return redirect("/message/{}".format(studentid))




@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='brown',
            email="brown@ga.com",
            password='123',
            fullname= 'Brown Katia',
            address='12 west street Oakland CA',
            phonenumber='2042334343',
            about='I have 5 years experience',
            profileImgUrl= 'https://www.opticalexpress.co.uk/images/feature-imgs/lady-with-glasses-smiling.jpg',
            role='teacher'
            )
        models.User.create_user(
            username='Jeff',
            email="jeff@ga.com",
            password='123',
            fullname= 'Jeff Habib',
            address='23 west street Oakland CA',
            phonenumber='212334390008',
            about='I have 2 years experience working with kids',
            profileImgUrl= 'http://interactive.nydailynews.com/2016/05/simpsons-quiz/img/simp1.jpg',
            role='teacher'
            )
        models.User.create_user(
            username='nassBouz',
            email='bouzianenassima@gmail.com',
            fullname ='Nassima Bouz ',
            password='123',
            profileImgUrl='http://thewildmagazine.com/wp-content/uploads/2012/01/DSC5526-copy.jpeg',
            phonenumber='51090095454',
            address='44 North Street West Oakland ca',
            about='here',
            role='parent'
            )
        models.User.create_user(
            username='zola',
            email='zola@gmail.com',
            fullname ='Cherik Zola',
            password='123',
            profileImgUrl='https://www.rd.com/wp-content/uploads/2017/09/01-shutterstock_476340928-Irina-Bg-1024x683.jpg',
            phonenumber='510900667754',
            address='122 west Oakland ca',
            about='sweet',
            role='parent'
            )
        models.Student.create_student(
            teacher=1,
            parent=3,
            fullname='Bouz Yanni',
            gender='male',
            dateOfBirth='03-04-2013',
            profileImgUrl='https://images.theconversation.com/files/50558/original/t739v7sc-1402311181.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=926&fit=clip',
            phonenumber='9259002323',
            address='44 North Street West Oakland ca',
            medicalNeeds='Peanut allergy',
            otherDetails='OTHER STUFFS'
            )
        models.Student.create_student(
            teacher=1,
            parent=4,
            fullname='Cherik Zira',
            gender='female',
            dateOfBirth='03-04-2012',
            profileImgUrl='https://static1.bigstockphoto.com/4/3/2/large1500/234733213.jpg',
            phonenumber='9259001111',
            address='122 west Oakland ca',
            medicalNeeds='Peanut allergy',
            otherDetails='OTHER STUFFS'
            )
        models.Student.create_student(
            teacher=2,
            parent=4,
            fullname='Cherik Fazia',
            gender='female',
            dateOfBirth='03-04-2015',
            profileImgUrl='http://i0.wp.com/sguru.org/wp-content/uploads/2017/02/cute-girls-profile-pics-for-facebook-13.jpg',
            phonenumber='9259001111',
            address='122 west Oakland ca',
            medicalNeeds='no allergies',
            otherDetails='OTHER STUFFS'
            )
        models.Message.create_message(
            sender=1,
            recipient=3,
            student=1,
            title="Bad behavior",
            text="your son is recently behaving really bad !! please take action or i am gonna take disciblinary actions ",
            imageUrl="none",
            imageFile='nothing',
            red=False
            )
    except ValueError:
        pass

    app.run(debug=DEBUG, port=PORT)