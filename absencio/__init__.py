from flask import Flask, url_for, render_template, request, session, flash, redirect
from os import path
import os
import sqlite3
import util.database as data
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = os.urandom(32)

DIR = path.dirname(__file__)

##########not sure if this is needed#######################
#f="absence_sys.db"
'''
f="var/www/absencio/absencio/absence_sys.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops '''

#console output will appear in /var/log/apache2/error.log


###############NOTES
'''

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

Email archive, sign a form and it emails you all the previous forms you have signed.

Oauth to verify stuy.edu emails, ask for minimal permissions, access info on these accounts.



STUDENT TO PARENT TABLE
Each entry is a student, column 1 is parent 1, column 2 is parent 2


'''
###############NOTES

@app.route('/')
def root():
    if in_session():
        if is_student():
            pending = data.retrieve_absences_by_student( session["user_id"], "pending" )
            history = data.retrieve_absences_by_student( session["user_id"], "history" )
            print pending
        if is_teacher():
            pending = data.retrieve_absences_by_teacher( session["user_id"], "pending")
            history = data.retrieve_absences_by_teacher( session["user_id"], "history" )
        return render_template('index.html', user_id = session["user_id"], first_name = session["first_name"], last_name = session["last_name"], email = session["email"], type = session["type"], in_session = in_session(), is_student = is_student(), is_parent = is_parent(), is_teacher = is_teacher(), dir = DIR, pending = pending, history = history)
    return render_template('signin.html')


######################################### Student Link to Parent
@app.route('/link_parent_account', methods=['POST'])
def link_parent_account():
    if in_session():
        if (request.form['parent_email'] == request.form['confirm_email']):
            print "the emails are the same!"
            data.add_parent_account( session['user_id'], request.form['parent_email'] )
            return redirect(url_for("root"))
        return render_template("failed_login.html", error = "EMAILS WERE DIFFERENT")
    return redirect(url_for("root"))

@app.route('/signin')
def signin():
    print request.method
    if 'user_id' in session:
        return redirect(url_for('root'));
    return render_template('signin.html')

##this solely serves as a redirect page
@app.route('/login', methods=['POST','GET'])
def login():
    #if a form hasn't been submitted
    if request.method == 'GET':
        return redirect(url_for("signin"))
    '''
    if request.form["email"].find("@stuy.edu") == -1:
        print "NEEDS TO BE A STUY.EDU EMAIL"
        pass
        return render_template('failed_login.html', error = "Need Stuy.edu email") #add error message as a parameter
    '''
    user = data.check_account(request.form)
    if user[0]:
        print "logged"
        session['user_id'] = user[1]
        session['first_name'] = user[2]
        session['last_name'] = user[3]
        session['email'] = user[4]
        session['type'] = int(user[5])
        session['osis'] = user[6]
        session['parent_email'] = user[7]
        print user[7]
        print "logged2"
        #session['user'] = request.form['email'][ : request.form['email'].find("@")]
        #session['type'] = data.check_account( request.form['email'], request.form['password'] )[1]
        #flash('You were logged in')
        return url_for('root')
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
        session.pop('user_id')
        session.pop('first_name')
        session.pop('last_name')
        session.pop('email')
        session.pop('type')
        session.pop('osis')
        session.pop('parent_email')
        return redirect(url_for('root'))
    return render_template("failed_login.html", error = "YOU WERE NEVER LOGGED IN" )


############# END OF ADMINISTRATIVE LOGIN HANDLING #############################



############# BEGINNING OF ROUTES FOR LOGGED IN ACCOUNTS #################

@app.route('/notes_queue_pending')
def notes_queue_pending():
    if in_session():
        if is_student():
            absences = data.retrieve_absences_by_student( session["user_id"], "pending" )
        if is_teacher():
            absences = data.retrieve_absences_by_teacher( session["user_id"], "pending")
        return render_template("notes_queue_pending.html", all_absences = absences)
    return redirect(url_for("root"))

@app.route('/notes_queue_history')
def notes_queue_history():
    if in_session():
        if is_student():
            absences = data.retrieve_absences_by_student( session["user_id"], "history" )
        if is_teacher():
            absences = data.retrieve_absences_by_teacher( session["user_id"], "history")
        return render_template("notes_queue_history.html", all_absences = absences)
    return redirect(url_for("root"))

######STUDENTS
@app.route('/new_form')
def new_form():
    if in_session():
        list = data.get_teacher_names()
        #list.append("Bob")
        return render_template("new_form.html", teacher_list = list)
    return redirect(url_for("root"))


@app.route('/submit_form' , methods=['POST','GET'])
def submit_form():
    print "on submit form"
    if in_session():

        #dict = {}
        #dict[request.form["course_one"]] = request.form["teacher_one"]
        #dict[request.form["course_two"]] = request.form["teacher_two"]
        #dict[request.form["course_three"]] = request.form["teacher_three"]
        #dict[request.form["course_four"]] = request.form["teacher_four"]
        #dict[request.form["course_five"]] = request.form["teacher_five"]
        #dict[request.form["course_six"]] = request.form["teacher_six"]
        #dict[request.form["course_seven"]] = request.form["teacher_seven"]
        #dict[request.form["course_eight"]] = request.form["teacher_eight"]
        #dict[request.form["course_nine"]] = request.form["teacher_nine"]
        #dict[request.form["course_ten"]] = request.form["teacher_ten"]

        class_list = []
        class_list.append( [ request.form["course_one"], request.form["teacher_one"] ] )
        class_list.append( [ request.form["course_two"], request.form["teacher_two"] ] )
        class_list.append( [ request.form["course_three"], request.form["teacher_three"] ] )
        class_list.append( [ request.form["course_four"], request.form["teacher_four"] ] )
        class_list.append( [ request.form["course_five"], request.form["teacher_five"] ] )
        class_list.append( [ request.form["course_six"], request.form["teacher_six"] ] )
        class_list.append( [ request.form["course_seven"], request.form["teacher_seven"] ] )
        class_list.append( [ request.form["course_eight"], request.form["teacher_eight"] ] )
        class_list.append( [ request.form["course_nine"], request.form["teacher_nine"] ] )
        class_list.append( [ request.form["course_ten"], request.form["teacher_ten"] ] )

        print "are you working here?"

        #need to add way to connect student and parent accounts
        note_id = data.new_note( request.form["osis"], session["user_id"], 99, request.form["excuse"], 1, 0, request.form["date"], 0, class_list);

        #emailParent() Use Session["parent_email"] for parent email
        sendemail(from_addr    = 'absencio.stuy@gmail.com',
                  to_addr_list = [session['parent_email']],
                  #cc_addr_list = ['ibnuljahan@gmail.com'],
                  cc_addr_list = [],
                  subject      = 'New Absent Note Available',
                  message      = 'Hello, your child just created a new absent/lateness excuse note. Please view/sign it here: http://absencio.stuycs.org/parent_sign/' + str(note_id) + ' or here: absencio.stuycs.org/parent_sign/' + str(note_id) + '',
                  login        = 'absencio.stuy',
                  password     = '@bsencio1')


    return redirect(url_for("root"))


@app.route('/display_note' , methods=['GET'])
@app.route('/display_note/<int:note_id>', methods=['POST'])
def display_note(note_id = 0):
    if in_session():
        if request.method == "POST" and is_teacher():
            print "Teacher signin"
            data.teacher_sign_note(note_id, session["user_id"])
            print "TEACHER SIGNED NOTE: " + str(note_id)
            return redirect(url_for('root'))
        print request.args.get("id")
        id = request.args.get("id")
        note = data.retrieve_absent_note( id )
        note = list(note)
        new_note = []
        for period in note:
            new_note.append(list(period))
        for period in range(len(new_note)):
            for datap in range(len(new_note[period])):
                if datap == 1:
                    name = data.retrieve_teacher_name_by_id(new_note[period][datap])
                    new_note[period][datap] = name[0] + " " + name[1]
                if datap == 3:
                    d = {1: "Yes", 0: "No"}
                    new_note[period][datap] = d[new_note[period][datap]]
        return render_template("display_note.html", id = id, note = new_note, is_student = is_student(), is_parent = is_parent(), is_teacher = is_teacher())
    return redirect(url_for("root"))

#####PARENTS

def emailParent(parent_email):
    msg = MIMEText("hello world email")
    msg['Subject'] = 'Absence note'
    msg['From'] = "calebsmithsalzberg@gmail.com"
    msg['To'] = parent_email
    s = smtplib.SMTP('localhost:5000')
    s.sendmail(me, [you], msg.as_string())
    s.quit()

@app.route('/parent_sign/<int:note_id>', methods=['POST','GET'])
def parent_sign(note_id):
    if request.method == "POST":
        data.parent_sign_note(note_id)
        print "PARENT SIGNED NOTE: " + str(note_id)
        return redirect(url_for('root'))
    else:
        note = data.retrieve_absent_note( note_id )
        note = list(note)
        new_note = []
        for period in note:
            new_note.append(list(period))
        for period in range(len(new_note)):
            for datap in range(len(new_note[period])):
                if datap == 1:
                    name = data.retrieve_teacher_name_by_id(new_note[period][datap])
                    new_note[period][datap] = name[0] + " " + name[1]
                if datap == 3:
                    d = {1: "Yes", 0: "No"}
                    new_note[period][datap] = d[new_note[period][datap]]
        return render_template("display_note.html", id = note_id, note = new_note, is_parent = True, is_teacher = False)

#####TEACHERS



###HELPER FUNCTIONS###
def in_session():
    bool = 'user_id' in session
    print "In session: " + str(bool)
    return bool

def is_student():
    if in_session():
        bool = session['type'] == 0
        print "Is Student: " + str(bool)
        return bool
def is_parent():
    if in_session():
        bool = session['type'] == 1
        print "Is Parent: " + str(bool)
        return bool
def is_teacher():
    if in_session():
        bool = session['type'] == 2
        print "Is Teacher: " + str(bool)
        return bool


def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems



if __name__ == '__main__':
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
