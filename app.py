from flask import Flask, g
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from werkzeug.utils import secure_filename
import os
import models 
import forms 
import json
from keyEcole import secret_key, MAIL_USERNAME , MAIL_PASSWORD ,MAIL_SERVER
# for mail alert
from flask_mail import Mail, Message
import json


DEBUG = True
PORT = 8000

app = Flask(__name__,instance_relative_config=True)


# //////////// mail setup/////////////
app.config['MAIL_SERVER']= MAIL_SERVER
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL_USERNAME 
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.secret_key = secret_key
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

def handle_signin(form):
    try:
        user = models.User.get(models.User.email == form.email.data)
    except models.DoesNotExist:
        flash("your email or password doesn't match", "error")
    else:
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have successfully Signed', 'success')
            return redirect(url_for('index'))
        else:
            flash("your email or password doesn't match", "error")

# landing page 
@app.route('/', methods=['GET', 'POST'])
def index():
    sign_in_form = forms.SignInForm()
    if sign_in_form.validate_on_submit():
        handle_signin(sign_in_form)
        return redirect(url_for('mySchool'))
    return render_template('auth.html', sign_in_form=sign_in_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    # return redirect(url_for('index'))
    return redirect(url_for('mySchool'))
# teacher profile
@app.route('/teacherprofile/<userid>', methods=['GET'])
def profilepage(userid):
    user = models.User.get(models.User.id == int(userid))
    students = models.Student.select().where(models.Student.teacher_id==int(user.id))
    messages = models.Message.select().where(models.Message.recipient_id == int(userid))
    return render_template('teacher.html', user=user ,students=students, messages=messages) 
# parent profile
@app.route('/parentprofile/<userid>', methods=['GET'])
def parentpage(userid):
    user = models.User.get(models.User.id == int(userid))
    students = models.Student.select().where(models.Student.parent_id==int(user.id))
    messages = models.Message.select().where(models.Message.recipient_id == int(userid))
    return render_template('parent.html', user=user,students=students, messages=messages)

# rendering messages and sending email alert
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
                msg = Message("Hi, your have a new message from ",sender=senderEmail,recipients=[receiverEmail])
                msg.body = f'Hello {student.parent.fullname}, {user.fullname} has sent you this message : {form.text.data}'
                mail.send(msg)
                flash("Your message has successefully been sent" , "success")
                return redirect("/message/{}".format(studentid))
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
                msg = Message("Hello , your have a new message from ",sender=senderEmail,recipients=[receiverEmail])
                msg.body = f'Hello {student.parent.fullname}, {user.fullname} has sent you this message : {form.text.data}'
                mail.send(msg)
                flash("Your message has successefully been sent" , "success")
                return redirect("/message/{}".format(studentid))
        return render_template('student.html',form=form ,student=student, user=user, messages=messages)

#edit student informations by teacher
@app.route('/edit-student/<studentid>', methods=['GET','POST'])
def edit_student(studentid=None):
    student = models.Student.select().where(models.Student.id == int(studentid)).get()
    formedit = forms.EditStudent()
    student.studentLevel = formedit.studentLevel.data
    student.workingOn = formedit.workingOn.data
    student.save()
    flash('Your changes have been saved', 'success')
    return redirect("/message/{}".format(studentid))
    
#edit student informations by parent
@app.route('/edit-student-parent/<studentid>', methods=['GET','POST'])
def edit_student_parent(studentid=None):
    student = models.Student.select().where(models.Student.id == int(studentid)).get()
    formStudent = forms.EditStudentParent()
    student.medicalNeeds = formStudent.medicalNeeds.data
    student.phonenumber = formStudent.phonenumber.data
    student.save()
    flash('Your changes have been saved', 'success')
    return redirect("/message/{}".format(studentid))

# edit own message by parent or teacher
@app.route('/edit-message/<messageid>', methods=['GET','POST'])
def edit_message(messageid=None):
    message_id = int(messageid)
    message = models.Message.get(models.Message.id == message_id)
    studentid = message.student_id
    student = models.Student.get_by_id(int(studentid))
    user = g.user._get_current_object()
    form = forms.MessageForm()
    if form.validate_on_submit():
        message.title= form.title.data
        message.text= form.text.data
        message.imageFile=form.imageFile.data
        message.imageUrl=form.imageUrl.data
        message.save()
        flash('Your changes have been saved.', 'success')
        return redirect("/message/{}".format(studentid))
    if message != None:
        form.title.data = message.title
        form.text.data = message.text
        form.imageFile.data = message.imageFile
        form.imageUrl.data = message.imageUrl
    
    return render_template('student.html',form=form ,student=student,user=user, message=message)
    

# delete message by owner
@app.route('/message/<messageid>/delete')
def delete_message(messageid):
    message_id = int(messageid)
    message = models.Message.get(models.Message.id == message_id)
    studentid = message.student_id
    message.delete_instance()
    flash("message successfully deleted ", "success")
    return redirect("/message/{}".format(studentid))

# school page 
@app.route('/mySchoolPage/', methods=['GET'])
def mySchool():
    # students = models.Student.select().where(models.Student.teacher_id==int(user.id))
    teachers = models.User.select().where(models.User.role == 'teacher')
    # user = models.User.get(models.User.id == int(userid))
    events = models.Event.select().limit(100)
    return render_template('mySchool.html',teachers=teachers, events=events) 


@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')


if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()


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
        models.User.create_user(
            username='Admin',
            email='admin@gmail.com',
            fullname ='Admin Man',
            password='123',
            profileImgUrl='https://www.lincolntech.edu/news/wp-content/uploads/2015/04/computer-specialist-tw.jpg',
            phonenumber='5109006656556',
            address='122 west Oakland ca',
            about='sweet',
            is_admin='True',
            role='teacher'
            )
        models.User.create_user(
            username='Domrane',
            email='malika@gmail.com',
            fullname ='Malike Domarane',
            password='123',
            profileImgUrl='https://i.ytimg.com/vi/I-rzGhDyefo/maxresdefault.jpg',
            phonenumber='92590095454',
            address='54 west Street San Ramon ca',
            about='I am a singer',
            role='parent'
            )
        models.User.create_user(
            username='Matoub',
            email='matoub@gmail.com',
            fullname ='Matoub Lounes',
            password='123',
            profileImgUrl='data:image/jpeg;base64,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',
            phonenumber='92590095454',
            address='3 Second Street Oakland CA',
            about='I am a writter',
            role='parent'
            )
        models.User.create_user(
            username='Lou',
            email='lou@gmail.com',
            fullname ='Lourdes Morales',
            password='123',
            profileImgUrl='https://ak2.picdn.net/shutterstock/videos/10547162/thumb/1.jpg',
            phonenumber='92390095454',
            address='Main street Berkley CA',
            about='I am a Thinker',
            role='parent'
            )
        models.Student.create_student(
            teacher=1,
            parent=8,
            fullname='Morales Jack',
            gender='male',
            dateOfBirth='11-08-2013',
            profileImgUrl='https://cdn.shopify.com/s/files/1/0879/4406/products/Jonas-Paul-Kids-Glasses-Solomon-Navy_grande.jpg?v=1530805624',
            phonenumber='92390095454',
            address='Main street Berkley CA',
            medicalNeeds='Dog allergy',
            otherDetails='OTHER STUFFS',
            studentLevel= 6,
            workingOn = 'Letters'
            )
        models.Student.create_student(
            teacher=1,
            parent=7,
            fullname='Matoub Eliana',
            gender='female',
            dateOfBirth='11-09-2014',
            profileImgUrl='https://designmag.fr/wp-content/uploads/2016/03/coiffure-petite-fille-cheveux-boucles.jpg',
            phonenumber='9259002323',
            address='3 Second Street Oakland CA',
            medicalNeeds='Cat allergy',
            otherDetails='OTHER STUFFS',
            studentLevel= 2,
            workingOn = 'Letters'
            )
        models.Student.create_student(
            teacher=1,
            parent=6,
            fullname='Domrane Rezki',
            gender='female',
            dateOfBirth='03-09-2013',
            profileImgUrl='data:image/jpeg;base64,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',
            phonenumber='9259002323',
            address='54 west Street San Ramon ca',
            medicalNeeds='Peanut allergy',
            otherDetails='OTHER STUFFS',
            studentLevel= 3,
            workingOn = 'Numbers'
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
            otherDetails='OTHER STUFFS',
            studentLevel= 3,
            workingOn = 'Numbers'
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
            otherDetails='OTHER STUFFS',
            studentLevel= 4,
            workingOn = 'Addition'
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
            otherDetails='OTHER STUFFS',
            studentLevel= 1,
            workingOn = 'Alphabet'
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
        models.Event.create_event(
            dateEvent='4-12-2019',
            title = 'Pijama Day',
            text='pijama day ',
            imgUrl ='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmqp-ShLSRkk3Nj-2634MaiUDJzJOIW7-59pKAH04vkmGquqCZ',
            priority='0'
            )
        models.Event.create_event(
            dateEvent='5-12-2019',
            title = 'Field Trip to Oakland Zoo',
            text='Field trip',
            imgUrl = 'https://www.marinmommies.com/sites/default/files/styles/full-width_column_827/public/stories/giraffes2.jpg?itok=m5H44a36',
            priority='0'
            )
        models.Event.create_event(
            dateEvent='4-26-2019',
            title = 'Good Friday',
            text='No school',
            imgUrl = 'https://p1cdn4static.sharpschool.com/UserFiles/Servers/Server_719363/Image/clip%20art/no%20school.jpg',
            priority='0'
            )
        
    except ValueError:
        pass

    app.run(debug=DEBUG, port=PORT)