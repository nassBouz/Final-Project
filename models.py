import datetime
import os
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('myEcole.db') 

# ------------------- ----------------------------------- #
# ------------------- Teacher Model --------------------- #
# ------------------- ----------------------------------- #
class User(UserMixin, Model):
    username = CharField(unique=True)
    fullname = CharField(max_length=120)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    about = TextField()
    joined_at = DateTimeField(default=datetime.datetime.now())
    address =CharField(max_length=120)
    is_admin = BooleanField(default=False)
    phonenumber = CharField(max_length=15)
    profileImgUrl = CharField(default='static/userDefault.png')
    role = CharField(max_length=120)
    
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        
    @classmethod
    def create_user(cls, username, email,fullname, password, profileImgUrl,phonenumber, address,about,role,is_admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                fullname =fullname,
                password=generate_password_hash(password),
                is_admin=is_admin,
                profileImgUrl=profileImgUrl,
                phonenumber=phonenumber,
                address=address,
                about=about,
                role=role
            )
        except IntegrityError:
            raise ValueError("user already exists")

    def get_students(self):
        return Student.select().where((Student.user == self))


# ------------------- ----------------------------------- #
# ------------------- Student Model --------------------- #
# ------------------- ----------------------------------- #
class Student(Model):
    # foreign key teacher 
    teacher = ForeignKeyField( 
        model=User, 
        backref='students'
    )
    # foreign key parent 
    parent = ForeignKeyField(
        model=User, 
        backref='students'
    ) 
    fullname = CharField(max_length=120)
    gender= CharField(max_length=12)
    dateOfBirth= DateField()
    otherDetails = TextField()
    joined_at = DateTimeField(default=datetime.datetime.now())
    address =CharField(max_length=120)
    medicalNeeds= CharField(max_length=300)
    phonenumber = CharField(max_length=15)
    profileImgUrl = CharField(default='static/userDefault.png')
    studentLevel= IntegerField(default=0)
    workingOn = CharField()
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        
    @classmethod
    def create_student(cls,teacher,parent,fullname,gender, dateOfBirth, profileImgUrl,phonenumber, address,medicalNeeds, otherDetails,studentLevel,workingOn):
        try:
            cls.create(
                teacher=teacher,
                parent=parent,
                fullname =fullname,
                gender=gender,
                dateOfBirth=dateOfBirth,
                profileImgUrl=profileImgUrl,
                phonenumber=phonenumber,
                address=address,
                medicalNeeds=medicalNeeds,
                otherDetails=otherDetails,
                workingOn=workingOn,
                studentLevel=studentLevel
            )
        except IntegrityError:
            raise ValueError("Student already exists")
        except Error:
            raise print('create error')

# ------------------- ----------------------------------- #
# ------------------- Classe Model --------------------- #
# ------------------- ----------------------------------- #
class Classe(Model):
    teacher = ForeignKeyField( 
        model=User, 
        backref='classes'
    )
    classname = CharField(max_length=120)
    created_at = DateTimeField(default=datetime.datetime.now())
    grad= IntegerField()
    classroomNumber = IntegerField()
    start_from = DateField()
    end_date= DateField()

    class Meta:
        database = DATABASE
        order_by = ('-created_at',)
        
    @classmethod
    def create_classe(cls,teacher,classname,grad,classroomNumber, profileImgUrl,start_from,end_date):
        try:
            cls.create(
                classname = classname,
                grad=grad,
                teacher=teacher,
                classroomNumber=classroomNumber,
                profileImgUrl=profileImgUrl,
                start_from=start_from,
                end_date=end_date
            )
        except IntegrityError:
            raise ValueError("class already exists")

# ------------------- ----------------------------------- #
# ------------------- Message Model --------------------- #
# ------------------- ----------------------------------- #
class Message(Model):
    # foreign key teacher 
    recipient = ForeignKeyField( model=User,backref='messages')
    student = ForeignKeyField( model=Student,backref='messages')
    # foreign key parent 
    sender = ForeignKeyField( model=User,backref='messages') 
    title = TextField()
    text = TextField()
    mesageDate = DateTimeField(default=datetime.datetime.now())
    imageUrl = CharField(default="noImage")
    imageFile=CharField()
    red= BooleanField(default=False)
    class Meta:
        database = DATABASE
        order_by = ('mesageDate',)
        
    @classmethod
    def create_message(cls,recipient,sender,title, text,imageUrl,imageFile,student,red=False):
        try:
            cls.create(
                recipient=recipient,
                sender=sender,
                title=title,
                text=text,
                imageUrl=imageUrl,
                imageFile=imageFile,
                student=student,
                red=red 
            )
        except IntegrityError:
            raise ValueError("message already exists")
# ------------------- ----------------------------------- #
# ------------------- StudentClass Model --------------------- #
# ------------------- ----------------------------------- #
class StudentClasse(Model):
    classe = ForeignKeyField( model=Classe,backref='StudentClasses')
    student= ForeignKeyField( model=Student,backref='StudentClasses')
    dateFrom = DateField()
    dateTo= DateField()
    dateCreated= DateTimeField(default=datetime.datetime.now())
   
    class Meta:
        database = DATABASE
        order_by = ('-dateCreated',)
        
    @classmethod
    def create_studentClasse(cls,classe,student,dateFrom,dateTo,dateCreated,studentLevel):
        try:
            cls.create(
                classe=classe,
                student=student,
                dateFrom=dateFrom,
                dateTo=dateTo,
                dateCreated=dateCreated,
                studentLevel=studentLevel
            )
        except IntegrityError:
            raise ValueError("studentClass already exists")

# ------------------- ----------------------------------- #
# ------------------- Post Model --------------------- #
# ------------------- ----------------------------------- #

class Event(Model):
    dateEventCreated = DateTimeField(default=datetime.datetime.now())
    # user = ForeignKeyField(
    #     model=User,
    #     backref='events'
    # )
    dateEvent = DateField()
    title = TextField()
    text = TextField()
    imgUrl = CharField()
    priority = IntegerField(default=0)

    class Meta:
        database = DATABASE
        order_by = ('-priority',)
    @classmethod
    def create_event(cls,dateEvent,title,text,imgUrl,priority):
        try:
            cls.create(
                dateEvent=dateEvent,
                title=title,
                text=text,
                imgUrl=imgUrl,
                priority=priority
            )
        except IntegrityError:
            raise ValueError("event already exists")

class UserUpVote(Model):
    user_id= IntegerField()
    event_id= IntegerField()
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,Classe,Message,StudentClasse,Student, UserUpVote,Event], safe=True)
    DATABASE.close()  