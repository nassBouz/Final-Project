import datetime
import os
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('myEcole.db') 

# ------------------- ----------------------------------- #
# ------------------- Teacher Model --------------------- #
# ------------------- ----------------------------------- #
class Teacher(UserMixin, Model):
    username = CharField(unique=True)
    fullname = CharField(max_length=120)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    biography = TextField()
    joined_at = DateTimeField(default=datetime.datetime.now())
    address =CharField(max_length=120)
    is_admin = BooleanField(default=False)
    phonenumber = CharField(max_length=15)
    profileImgUrl = CharField(default='static/userDefault.png')
    
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        
    @classmethod
    def create_teacher(cls, username, email,fullname, password, profileImgUrl,phonenumber, address,biography,admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                fullname =fullname,
                password=generate_password_hash(password),
                is_admin=admin,
                profileImgUrl=profileImgUrl,
                phonenumber=phonenumber,
                address=address,
                biography=biography
            )
        except IntegrityError:
            raise ValueError("Teacher already exists")

    def get_students(self):
        return Student.select().where((Student.teacher == self))



# ------------------- ----------------------------------- #
# ------------------- Parent Model --------------------- #
# ------------------- ----------------------------------- #
class Parent(UserMixin, Model):
    username = CharField(unique=True)
    fullname = CharField(max_length=120)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    about = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now())
    address =CharField(max_length=120)
    is_admin = BooleanField(default=False)
    phonenumber = CharField(max_length=15)
    profileImgUrl = CharField(default='static/userDefault.png')
    
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        
    @classmethod
    def create_parent(cls, username, email,fullname, password, profileImgUrl,phonenumber, address,about,admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                fullname =fullname,
                password=generate_password_hash(password),
                is_admin=admin,
                profileImgUrl=profileImgUrl,
                phonenumber=phonenumber,
                address=address,
                about=about
            )
        except IntegrityError:
            raise ValueError("Parent already exists")

# ------------------- ----------------------------------- #
# ------------------- Student Model --------------------- #
# ------------------- ----------------------------------- #
class Student(Model):
    # foreign key teacher 
    teacher = ForeignKeyField( 
        model=Teacher, 
        backref='students'
    )
    # foreign key parent 
    parent = ForeignKeyField(
        model=Parent, 
        backref='students'
    ) 
    fullname = CharField(max_length=120)
    gender= CharField(max_length=12)
    # change date 
    dateOfBirth= DateField()
    otherDetails = TextField()
    joined_at = DateTimeField(default=datetime.datetime.now())
    address =CharField(max_length=120)
    medicalNeeds= CharField(max_length=300)
    phonenumber = CharField(max_length=15)
    profileImgUrl = CharField(default='static/userDefault.png')
   
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        
    @classmethod
    def create_student(cls,teacher,parent,fullname,gender, dateOfBirth, profileImgUrl,phonenumber, address,medicalNeeds, otherDetails):
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
                otherDetails=otherDetails
            )
        except IntegrityError:
            raise ValueError("Student already exists")
        except Error:
            raise print('create error')

# ------------------- ----------------------------------- #
# ------------------- Classe Model --------------------- #
# ------------------- ----------------------------------- #
class Classe(Model):
    classname = CharField(max_length=120)
    joined_at = DateTimeField(default=datetime.datetime.now())
    grad= IntegerField()
    classroomNumber = IntegerField()
    profileImgUrl = CharField(default='static/userDefault.png')
    start_from = DateField()
    end_date= DateField()

   
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        
    @classmethod
    def create_classe(cls,classname,grad,classroomNumber, profileImgUrl,start_from,end_date):
        try:
            cls.create(
                classname = classname,
                grad=grad,
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
    teacher = ForeignKeyField( model=Teacher,backref='messages')
    # foreign key parent 
    parent = ForeignKeyField( model=Parent,backref='messages') 
    title = TextField()
    text = TextField()
    mesageDate = DateTimeField(default=datetime.datetime.now())
    imageUrl = CharField()
    imageFile=CharField()
    red= BooleanField(default=False)
    class Meta:
        database = DATABASE
        order_by = ('-mesageDate',)
        
    @classmethod
    def create_message(cls,teacher,parent,title, text,imageUrl,imageFile,red=False):
        try:
            cls.create(
                teacher=teacher,
                parent=parent,
                title=title,
                text=text,
                imageUrl=imageUrl,
                imageFile=imageFile,
                red=red 
            )
        except IntegrityError:
            raise ValueError("message already exists")
# ------------------- ----------------------------------- #
# ------------------- StudentClass Model --------------------- #
# ------------------- ----------------------------------- #
class StudentClasse(Model):
    classe = ForeignKeyField( model=Classe,backref='StudentClasses')
    student= ForeignKeyField( model=Teacher,backref='StudentClasses')
    dateFrom = DateField()
    dateTo= DateField()
    dateCreated= DateTimeField(default=datetime.datetime.now())
    studentLevel= IntegerField()
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


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Teacher,Parent,Classe,Message,StudentClasse,Student], safe=True)
    DATABASE.close()  