# E-LEARNING

## Overview
e-learning is a free project carried out for the last project of  
the python developer path at OpenClassrooms.  
It is a free learning platform. Coming down to instructors who create courses  
and students who register for the desired courses and take them quietly.  

## Technologies used
This project required the use of *python* __(V3.8)__, the  
[Django __V3.1__](https://www.djangoproject.com) framework  
and some *javaScript/jQuery* to be achieved.

## How to run the project on local

1. ### First, clone or download the project on local
    - `git clone https://github.com/Vector22/elearning.git`

2. ### Install the required libraries
    - `cd /path/to/elearning`
    - `virtualenv -p python3.8 env` *you can use pyenv or venv*
    - `pip install -r requirements.txt` *to install the required libraries*

3. ### Run the database migrations
    - `source env/bin/activate`
    - `./python manage.py migrate`
    
4. ### Create a super user
    - The virtal environement is activated
    - `./python manage.py createsuperuser` *follow the steps to create it*

5. ### Run the server
    - `./python manage.py runserver`

6. ### Create Instructors and some students
    - The instructors can be created in the admin interface of the app.
      You just need to create a user and add it to the **Instructors** group.
    - After, you can create course in the admin panel or via the non admin
      panel. In the admin panel, just create courses and assing the rigth
      instructor to it. To the non admin panel, go to *localhost:8000* and try
      to login with the instructor account you created in the admin panel before.
      And follow the *Manage Courses* link. Create courses and then create modules
      for courses.
    - Students can be created by the *Register Now* link in the login page.

7. ### Try to explore the interface by yourself
    - The drag and drop feature is available for instructors to mange their
     courses and modules contents.
    - Instructors can also follow courses of others


## Always in built, send me feedback and errors by email on ***rekinvector@gmail.com***