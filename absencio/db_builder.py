import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import os #Used for os.remove()


#f= "absence_sys.db"
f= "absence_sys.db"
try:
    #pass
    os.remove(f) #Used During Testing to remove file at the beginning
except:
    pass

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops


def make_tables():
    #############USERS

    #type 0 is student, 1 is parent, 2 is teacher
    #user_id, username, password, first_name, last_name, email, type
    command= "CREATE TABLE users(user_id INTEGER, first_name TEXT, last_name TEXT, email TEXT, type INTEGER, osis TEXT)"
    c.execute(command);

    ###########PARENTS
    #student_id, parent1email, parent1id, parent1confirmation, parent2email, parent2id, parent2 confirmation
    command = "CREATE TABLE student_parent(student_id INTEGER, parent_1_email TEXT, parent_1_id INTEGER, parent_1_confirm INTEGER, parent_2_email TEXT, parent_2_id INTEGER, parent_2_confirm INTEGER)"
    c.execute(command);


     #############NOTES

    #integer 0 is false, 1 is true
    #id, osis, student_id, parent_id, explanation, signed_by_student, signed_by_parent, date, completed
    command= "CREATE TABLE absent_notes(id INTEGER, osis INTEGER, student_id INTEGER, parent_id INTEGER, explanation TEXT, signed_by_student INTEGER, signed_by_parent INTEGER, date BLOB, completed INTEGER )"
    c.execute(command);

    #############STUDENT SCHEDULES

    #student_id, pdA teacher, pdB teacher, ... , pdJ teacher
    command= "CREATE TABLE student_schedule(student_id INTEGER, pdA TEXT, pdB TEXT, pdC TEXT, pdD TEXT, pdE TEXT, pdF TEXT, pdG TEXT, pdH TEXT, pdI TEXT, pdJ TEXT)"
    c.execute(command);




#this makes an unactivated user
def new_user(email, first, last, type, osis):

    command = "SELECT COUNT(*) FROM users"
    c.execute(command)
    count = c.fetchone()[0]

    command = "INSERT INTO users VALUES(" + str(count) + ",'" + first + "','" + last + "','" + email + "'," + str(type) + ",'" + osis + "')"
    c.execute(command)

    if type==0:
        command = "INSERT INTO student_parent VALUES(" + str(count) + ",'','','','','','')"
        c.execute(command)

    return count

##############MAKES TABLE IF IT DOESNT EXIST ALREADY###################
try:
    make_tables();
except:
    pass


#new_user("ijahan1@stuy.edu", "ibnul", "jahan", 0, "274373333")
new_user("mrshenoy@stuy.edu", "teacher", "shenoy", 2, "")
#new_user("name", "pass")


db.commit() #save changes
db.close()  #close database
