from flask import Flask, url_for, render_template, request, session, flash, redirect
from os import path
import os
import sqlite3
import util.database as data

app = Flask(__name__)
app.secret_key = os.urandom(32)

DIR = path.dirname(__file__)

##########not sure if this is needed#######################
f="absence_sys.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#console output will appear in /var/log/apache2/error.log




###############NOTES
'''
Should we dump the whole db entry that is logged in into the session (minus the password)
This would be the username, first name, last name, email, and TYPE

Should type be number based (slight ease of coding) or string based (ease of reading)

Should account type differentiation be done through the flask and python or through the html and the templates
Either the python can redirect to one of MANY templates, customized for each account type
Or the html can all pull from a common base, but be heavily differentiated based on the account type
^^^I think the latter of the two will be used -- mention this in the devlog later

Should there be an activated? column in the database

Still need to set of droplet database stuff because that does not work

Absence notes have not been touched yet

Randomize activation codes at the gen of the database, and then retrieve them with a temporary or access-locked file at the beginning to distribute

Making an account is not really a thing (by design). All accounts should be made to start with, and should be activated by their account holders


'''
###############NOTES

















@app.route('/')
def root():
    if 'user' in session:
        return render_template('index.html', username = session['user'], in_session = in_session(), is_student = is_student(), is_parent = is_parent(), is_teacher = is_teacher(), dir = DIR)
    return render_template('index.html',  in_session = in_session(), is_student = is_student(), is_parent = is_parent(), is_teacher = is_teacher(), dir = DIR)
    

@app.route('/signup')
def signup():
    if 'user' in session:
        return redirect(url_for('root'));
    return render_template('signup.html')

##this solely serves as a redirect page
@app.route('/activate', methods=['POST'])
def activate():
   # if in_session():
        ###return render_template("create_password.html")
    #    pass
    
    if request.method == 'POST':
        if data.activateable(request.form['email'], request.form['code']):
            error = "Your account does exist"
            session['user'] = request.form['email'][ : request.form['email'].find("@")]
            session['type'] = data.check_account(request.form['email'], request.form['code'])[1]
            return render_template("create_password.html")
        else:
            return render_template("failed_login.html", error = "something wrong man")
    else:
        flash('You were logged in')
        return redirect(url_for('root'))
    return render_template('failed_login.html', error = error) #add error message as a parameter

@app.route('/create_password', methods=['POST'])
def create_password():
    if (request.form['password'] == request.form['password_verif']):
        print session['user'] , request.form['password'] 
        newpass = data.activate_account( session['user'] , request.form['password'] )
        return render_template("index.html", is_student = is_student(), is_parent = is_parent(), is_teacher = is_teacher(), username = session['user'], in_session = in_session(), dir = "Not a dir, but the new password is  ")
    return render_template("failed_login.html", error = "Passwords did not match")


@app.route('/signin')
def signin():
    print request.method
    if 'user' in session:
        return redirect(url_for('root'));
    return render_template('signin.html')


##this solely serves as a redirect page
@app.route('/login', methods=['POST','GET'])
def login():
    #if a form hasn't been submitted
    if request.method == 'GET':
        return redirect(url_for("signin"))
    if data.check_account( request.form['email'], request.form['password'] )[0]:
        session['user'] = request.form['email'][ : request.form['email'].find("@")]
        session['type'] = data.check_account( request.form['email'], request.form['password'] )[1]
        flash('You were logged in')
        return redirect(url_for('root'))
    return render_template('failed_login.html', error = "WRONG LOGIN INFO") #add error message as a parameter
    '''
    if request.form['email'].find("stuy.edu") == -1:
        error = 'Invalid email'
    elif request.form['password'] != "password":
        error = 'Invalid password'
    else:
        session['user'] = request.form['email'][ : request.form['email'].find("@")]
        flash('You were logged in')
        return redirect(url_for('root'))
    return render_template('failed_login.html', error = error) #add error message as a parameter
    '''

@app.route('/logout', methods=['POST','GET'])
def logout():
    if in_session():
        session.pop('user')
        return render_template("index.html", in_session = in_session(), is_student = is_student(), is_parent = is_parent(), is_teacher = is_teacher())
    return render_template("failed_login.html", error = "YOU WERE NEVER LOGGED IN" )


############# END OF ADMINISTRATIVE LOGIN HANDLING #############################



############# BEGINNING OF ROUTES FOR LOGGED IN ACCOUNTS #################

@app.route('/notes_queue')
def notes_queue():
    if in_session():
        return render_template("notes_queue.html")
    return render_template("index.html", is_student = is_student(), is_parent = is_parent(), is_teacher = is_teacher(), error = "You are not logged in")


######STUDENTS
@app.route('/new_form')
def new_form():
    if in_session():
        return render_template("new_form.html")
    return render_template("index.html", is_student = is_student(), is_parent = is_parent(), is_teacher = is_teacher(), error = "You are not logged in")

@app.route('/submit_form')
def submit_form():
    if in_session():
        return redirect(url_for(notes_queue))
    return render_template("index.html", is_student = is_student(), is_parent = is_parent(), is_teacher = is_teacher(), error = "You are not logged in")

#####PARENTS



#####TEACHERS



###HELPER FUNCTIONS###
def in_session():
    return 'user' in session 

def is_student():
    if in_session():
        return session['type'] == 0
def is_parent():
    if in_session():
        return session['type'] == 1
def is_teacher():
    if in_session():
        return session['type'] == 2

if __name__ == '__main__':
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
