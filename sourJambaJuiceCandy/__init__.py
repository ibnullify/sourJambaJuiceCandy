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

@app.route('/')
def root():
    if 'user' in session:
        return render_template('index.html', dir = DIR)
    return render_template('index.html', dir = DIR)
    

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
            return render_template("create_password.html")
    else:
        flash('You were logged in')
        return redirect(url_for('root'))
    return render_template('failed_login.html', error = error) #add error message as a parameter

@app.route('/create_password', methods=['POST'])
def create_password():
    if (request.form['password'] == request.form['password_verif']):
        data.activate_account( session['user'] , request.form['password'] )
        return render_template("index.html", dir = DIR)
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
    
    if request.form['email'].find("stuy.edu") == -1:
        error = 'Invalid email'
    elif request.form['password'] != "password":
        error = 'Invalid password'
    else:
        session['user'] = request.form['email'][ : request.form['email'].find("@")]
        flash('You were logged in')
        return redirect(url_for('root'))
    return render_template('failed_login.html', error = error) #add error message as a parameter


###HELPER FUNCTIONS###
def in_session():
    return 'user' in session 

if __name__ == '__main__':
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
