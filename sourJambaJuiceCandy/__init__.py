from flask import Flask, url_for, render_template, request, session, flash, redirect
from os import path
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(32)

DIR = path.dirname(__file__)


#console output will appear in /var/log/apache2/error.log

@app.route('/')
def root():
    print "=====================================\nConsole Message\n"
    print DIR + "\n====================================="
    body = "<h2> Deployment Test </h2>"
    body+= "DIR: " + DIR + "<br>"
    
    if 'user' in session:
        body += session['user']
    body+= '<img src="' + url_for('static', filename='img/jambajuice.png') + '" width="500"</img>'
    return body

@app.route('/signup')
def signup():
    if 'user' in session:
        return redirect(url_for('root'));
    return render_template('signup.html')

@app.route('/signin')
def signin():
    if 'user' in session:
        return redirect(url_for('root'));
    return render_template('signin.html')


##this solely serves as a redirect page
@app.route('/login', methods=['POST'])
def login():
    if request.form['email'].find("stuy.edu") == -1:
        error = 'Invalid email'
    elif request.form['password'] != "password":
        error = 'Invalid password'
    else:
        session['user'] = request.form['email'][ : request.form['email'].find("@")]
        flash('You were logged in')
        return redirect(url_for('root'))
    return render_template('failed_login.html', error = error) #add error message as a parameter


if __name__ == '__main__':
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
