import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import os #Used for os.remove()

f="absence_sys.db"
try:
    os.remove(f) #Used During Testing to remove file at the beginning
except:
    pass

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops


def make_tables():
    #type 0 is student, 1 is teacher, 2 is parent
    #user_id, username, password, first_name, last_name, email, type
    command= "CREATE TABLE users(user_id INTEGER, username TEXT, password TEXT, first_name TEXT, last_name TEXT, email TEXT, type INTEGER)"
    c.execute(command);

    #integer 0 is false, 1 is true
    #id, osis, student_id, parent_id, explanation, signed_by_student, signed_by_parent, date, completed
    command= "CREATE TABLE absent_notes(id INTEGER, osis INTEGER, student_id INTEGER, parent_id INTEGER, explanation TEXT, signed_by_student INTEGER, signed_by_parent INTEGER, date BLOB, completed INTEGER )"
    c.execute(command);
    
    ##command = "INSERT INTO users VALUES('a', 'a', 'a')"
    ##c.execute(command);


###################################THIS NEEDS REVAMPING#######################
def new_user(email, first, last, type):
    uname = email[ : email.find('@')]
    
    command = "SELECT COUNT(*) FROM users"
    c.execute(command)
    count = c.fetchone()[0]
    
    command = "INSERT INTO users VALUES(" + str(count) + ",'" + uname + "','" +  str(count) +"','" + first + "','" + last + "','" + email + "'," + str(type) +")"
    c.execute(command)


make_tables();
new_user("ijahan1@stuy.edu", "ibnul", "jahan", 0)
#new_user("name", "pass")


db.commit() #save changes
db.close()  #close database
