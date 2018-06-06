#!usr/bin/python

import os, sys, sqlite3

#f = "absence_sys.db"
f = "var/www/absencio/absencio/absence_sys.db"
db = sqlite3.connect(f)
c = db.cursor()

def get_db(): #returns connection to database
    return sqlite3.connect(f)

def get_cursor(db): #returns cursor to database
    return db.cursor()

def close(db): #commits to and closes database
    db.commit()
    db.close()

#creating the db is handled in ../db_builder.py

#============================================================#
#============================Users=========================#
#============================================================#


#This checks if the email, activation code combo works in the database
def activateable( email, activation_code ) :
    #f="absence_sys.db"
    db = get_db()
    c = get_cursor(db)

    command = "SELECT * FROM users WHERE email = '" + email + "'"
    c.execute(command);
    results = c.fetchall()
    ##results[x] is the xth entry
    ##results[x][y] is the yth column of the xth entry

    if (len(results) == 0):
        print "THAT EMAIL IS NOT ASSOCIATED WITH AN ACCOUNT!"
        close(db)
        return False

    print results, len(results), results[0], results[0][0]

    if (len(results) > 1):
        print "THERE EXISTS MORE THAN ONE ACCOUNT WITH THAT EMAIL. INTERNAL ERROR!"
        close(db)
        return False



    command = "SELECT * FROM users WHERE email = '" + email + "' AND password = '" + activation_code + "'"
    c.execute(command)
    results = c.fetchall()
    if (len(results)) == 0:
        print "YOUR ACTIVATION CODE IS WRONG"
        close(db)
        return False
    close(db)
    return True

##how do you update entries
def activate_account( username, newpass ):
    #f="absence_sys.db"
    db = get_db()
    c = get_cursor(db)
    #command = "SELECT password FROM users WHERE email = '" + email + "'"
    print newpass, username
    command = "UPDATE users SET password = '" + str(newpass) + "' WHERE username = '" + username + "'"
    c.execute(command);
    print db.commit()
    #results = c.fetchall()
    print "password updated"

    command = "SELECT password FROM users WHERE username = '" + username + "'"
    c.execute(command)

    ret = c.fetchall()[0]
    close(db)
    return ret

def check_account( email, password ):
    #f="absence_sys.db"
    db = get_db()
    c = get_cursor(db)
    command = "SELECT * FROM users WHERE email = '" + email + "' AND password = '" + password + "'"
    c.execute(command)
    results = c.fetchall()
    if (len(results) > 1):
        print "THERE ARE TWO IDENTICAL ACCOUNT LOGINS. INTERNAL ERROR"
        close(db)
        return False, False, False, False, False, False, False
    if (len(results) == 0):
        print "INCORRECT LOGIN"
        close(db)
        return False, False, False, False, False, False, False
    #user_id, username, first_name, last_name, email, type
    close(db)
    return True, results[0][0], results[0][1], results[0][3], results[0][4], results[0][5], results[0][6]

def add_parent_account( student_id, parent_email ):
    db = get_db()
    c = get_cursor(db)

    command = "SELECT COUNT(*) FROM users"
    c.execute(command)
    count = c.fetchone()[0]

    #command= "CREATE TABLE users(user_id INTEGER, username TEXT, password TEXT, first_name TEXT, last_name TEXT, email TEXT, type INTEGER)"

    command = "INSERT INTO users VALUES(" + str(count) + ",'','" + str(count) + "','','','" + parent_email + "', 1)"
    c.execute(command)

    command = "INSERT INTO student_parent VALUES(" + str(student_id) + ",'" + parent_email + "', " + str(count) + ", 0, '', -1, 0)"
    c.execute(command)

    db.commit()
    close(db)

#Returns a list of all teachers
def get_teacher_names():
    db = get_db()
    c = get_cursor(db)

    command = "SELECT * FROM users WHERE type='2';"
    teachers = [ [x[3].encode("utf-8"), x[4].encode("utf-8")] for x in c.execute(command).fetchall()]
    close(db)
    return teachers

#Takes in a first and last name
#Returns a teacher id
def retrieve_teacher_id_by_name(first_name, last_name):
    db = get_db()
    c = get_cursor(db)

    command = "SELECT user_id FROM users WHERE (first_name = ? AND last_name = ?);"
    id = c.execute(command, (first_name, last_name)).fetchone()

    if not id == None:
        if len(id) > 1:
            print "Multiple Teachers"
            return id
        return id[0]
    print "ERROR LOOKING UP TEACHER BY NAME"

#============================================================#
#============================Absence Notes=========================#
#============================================================#

#add to big notes db
#create individual note db
def new_note( osis, student_id, parent_id, explanation, signed_by_student, signed_by_parent, date, completed, class_list):

    #f="absence_sys.db"
    db = get_db()
    c = get_cursor(db)

    command = "SELECT COUNT(*) FROM absent_notes"
    c.execute(command)
    count = c.fetchone()[0]

    #this should add to the aggregate note table
    command = "INSERT INTO absent_notes VALUES(" + str(count) + "," + str(osis) + "," + str(student_id) + "," + str(parent_id) + ",'" + explanation + "'," + str(signed_by_student) + "," + str(signed_by_parent) + ",'" + date + "'," + str(completed) + ")"
    c.execute(command)

    print "added to big"

    #this should create an individual note table
    command = "CREATE TABLE note_" + str(count) + "( course_code TEXT, teacher_id INTEGER, period INTEGER, signed INTEGER )"
    c.execute(command)

    print "made small"

    #this should add to the individual note tables
    for i in xrange(10):
        print "insertion " + str(i)
        teacher_name = class_list[i][1].split(" ")
        print  "INSERT INTO note_" + str(count) + " VALUES('" + class_list[i][0] + "','" + str(retrieve_teacher_id_by_name(teacher_name[0], teacher_name[1])) + "'," + str(i + 1) + ",'' )"
        command = "INSERT INTO note_" + str(count) + " VALUES('" + class_list[i][0] + "','" + str(retrieve_teacher_id_by_name(teacher_name[0], teacher_name[1])) + "'," + str(i + 1) + ",0 )"
        c.execute(command)

        db.commit()

    close(db)
    print "added to small"

def retrieve_absences_by_student( user_id ):
    #f="absence_sys.db"
    db = get_db()
    c = get_cursor(db)

    command = "SELECT * FROM absent_notes WHERE student_id = " + str(user_id) + ""
    c.execute(command)

    results = c.fetchall()
    ##results[x] is the xth entry
    ##results[x][y] is the yth column of the xth entry
    close(db)
    return results

def retrieve_absent_note( note_id ):
    db = get_db()
    c = get_cursor(db)

    command = "SELECT * FROM note_" + str(note_id) + ""
    c.execute(command)

    results = c.fetchall()
    ##results[x] is the xth entry
    ##results[x][y] is the yth column of the xth entry
    close(db)
    return results





##class_list is a list of teachers for each period. FREE or LUNCH for a free or lunch

# TO ADD LATER: perhaps add another column for the course name, which will be matched with 
#the teachers schedule. So, if John says he has Mr. Smith for pd1, the course title will
#automatically be added to his saved schedule because Mr. Smith has added all his courses into 
#his schedule.

def student_sched_addition(student_id , class_list):
    db = get_db()
    c = get_cursor(db)

    command = "INSERT INTO student_schedule VALUES(" + student_id + "," + class_list[0] + "," + class_list[1] + "," + class_list[2] + "," + class_list[3] + "," + class_list[4] + "," + class_list[5] + "," + class_list[6] + "," + class_list[7] + "," + class_list[8] + "," + class_list[9] + " )"
    c.execute(command)



