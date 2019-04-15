## App name: myEcole 
![Screenshot ](../master/myEcole.png)


- School Page
![Screenshot ](../master/schoolpage.png)

- Parent Page 
![Screenshot ](../master/parentPage.png)



## Overview
myEcole simplifies communication between parents and teachers, by bringing together all communication solutions and features under one platform. Parents can view their kids improvements and grades ,they can message their kids' teachers. myEcole is a powerful tool for teacher to keep the parents updated and engaged in their kids improvements. 
-[myEcole](https://myecole-flask.herokuapp.com/)

## Technology used
- Flask
- Jinja2
- Python3
- SQLite Database
- WTForms
- Bootstrap
- Flask-Mail
- HTML5
- CSS3
- Flask-login
- Peewee

## Installation steps

### Virtualenv
Let's also build a virtual environment. Virtual environments allow us to have multiple versions of Python on the same system so we can have different versions of both Python and the packages we are using on our computers.

```$ git clone https://github.com/nassBouz/Final-Project.git```

```$ cd Final-Project```

```$ pip3 install virtualenv```

```$ virtualenv .env -p python3```

```$ source .env/bin/activate```

### Dependencies 

```$ pip3 install flask flask-login flask-bcrypt peewee flask-wtf```

```$ pip3 freeze > requirements.txt```

### The App
You will need to create a keyEcole.py that contains the following variables

 scret_key = "the secret key of your App"
 
 MAIL_USERNAME = "the email address that you use to send notifications from"
 
 MAIL_PASSWORD = " password of your email address"
 
 MAIL_SERVER = " by default is 'smtp.gmail.com' "

then just run :

```$git python3 app.py```


## Approach

User Story
- User can only login
- User can be teacher, parent or an administrator
- User will receive email notification when new message
- User logged in will be directed to the school page, where they can see general information about the school and upcoming events

Teacher
- logged in Teacher can go to their profile page and see the list of their students, and also edit/update their profile.
- Teacher can go to the student profile where they can update student informations, send/edit/delete/receive messages.

Parent 
- logged in Parent can go to their profile page and see the list of their kids, and also edit/update their profile.
- Parent can go to the student profile where they can update student informations, send/edit/delete/receive messages.
 
## ERD (Entity Relationship Diagram)
 ![Screenshot ](../master/IMG_2566.JPG)
 
## Wireframes
 ![Screenshot ](../master/IMG_2863.JPG)
 
## Screen Shots 
![Screenshot ](../master/errorhandling.png)

![Screenshot ](../master/displayStudents.png)
 
## Biggest Wins and Challenges
- Learning Flask in depth
- Time management and prioritazing my tasks



## Future Features
- Admin page to create classes, assign students , parents and teachers
- Class page where users can connect and post.

## Thank you 
To everyone, especially the instructors Brock , Isha, and Dalton
