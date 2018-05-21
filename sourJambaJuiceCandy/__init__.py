from flask import Flask, url_for
from os import path

app = Flask(__name__)

DIR = path.dirname(__file__)


#console output will appear in /var/log/apache2/error.log

@app.route('/')
def root():
    print "=====================================\nConsole Message\n"
    print DIR + "\n====================================="
    body = "<h2> Deployment Test </h2>"
    body+= "DIR: " + DIR + "<br>"
    body+= '<img src="' + url_for('static', filename='img/jambajuice.png') + '" width="500"</img>'
    return body

@app.route('/signup')
def signup():
    body = "You should be provided an account/activation code from your teacher"
    body += "<br>"
    body+= "Insert form for making stuff here"
    return body


if __name__ == '__main__':
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
