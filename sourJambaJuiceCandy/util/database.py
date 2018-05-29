#!usr/bin/python

import os, sys, sqlite3

f="absence_sys.db"
db = sqlite3.connect(f)
c = db.cursor()    

#creating the db is handled in ../db_builder.py

#This checks if the email, activation code combo works in the database
def activateable( email, activation_code ) :
    f="absence_sys.db"
    db = sqlite3.connect(f) 
    c = db.cursor()
    
    command = "SELECT * FROM users WHERE email = '" + email + "'"
    c.execute(command);
    results = c.fetchall()
    ##results[x] is the xth entry
    ##results[x][y] is the yth column of the xth entry

    if (len(results) == 0):
        print "THAT EMAIL IS NOT ASSOCIATED WITH AN ACCOUNT!"
        return False
    
    print results, len(results), results[0], results[0][0]
    
    if (len(results) > 1):
        print "THERE EXISTS MORE THAN ONE ACCOUNT WITH THAT EMAIL. INTERNAL ERROR!"
        return False
    
    
    
    command = "SELECT * FROM users WHERE email = '" + email + "' AND password = '" + activation_code + "'"
    c.execute(command)
    results = c.fetchall()
    if (len(results)) == 0:
        print "YOUR ACTIVATION CODE IS WRONG"
        return False
    return True

##how do you update entries
def activate_account( username, newpass ):
    f="absence_sys.db"
    db = sqlite3.connect(f) 
    c = db.cursor() 
    #command = "SELECT password FROM users WHERE email = '" + email + "'"
    print newpass, username
    command = "UPDATE users SET password = '" + str(newpass) + "' WHERE username = '" + username + "'"
    c.execute(command);
    print db.commit()
    #results = c.fetchall()
    print "password updated"

    command = "SELECT password FROM users WHERE username = '" + username + "'"
    c.execute(command)
    
    return c.fetchall()[0]


def check_account( email, password ):
    f="absence_sys.db"
    db = sqlite3.connect(f) 
    c = db.cursor() 
    command = "SELECT * FROM users WHERE email = '" + email + "' AND password = '" + password + "'"
    c.execute(command)
    results = c.fetchall()
    if (len(results) > 1):
        print "THERE ARE TWO IDENTICAL ACCOUNT LOGINS. INTERNAL ERROR"
        return False, False, False, False, False, False, False
    if (len(results) == 0):
        print "INCORRECT LOGIN"
        return False, False, False, False, False, False, False
    #user_id, username, first_name, last_name, email, type
    return True, results[0][0], results[0][1], results[0][3], results[0][4], results[0][5], results[0][6]
    

#add to big notes db
#create individual note db
def new_note( osis, student_id, parent_id, explanation, signed_by_student, signed_by_parent, date, completed, class_list):

    f="absence_sys.db"
    db = sqlite3.connect(f) 
    c = db.cursor() 

    command = "SELECT COUNT(*) FROM absent_notes"
    c.execute(command)
    count = c.fetchone()[0]
    
    #this should add to the aggregate note table
    command = "INSERT INTO absent_notes VALUES(" + str(count) + "," + str(osis) + "," + str(student_id) + "," + str(parent_id) + ",'" + explanation + "'," + str(signed_by_student) + "," + str(signed_by_parent) + ",'" + date + "'," + str(completed) + ")"
    c.execute(command)

    print "added to big"
    
    #this should create an individual note table
    command = "CREATE TABLE note_" + str(count) + "( course_code TEXT, teacher TEXT, period INTEGER, signed INTEGER )"
    c.execute(command)

    print "made small"
    
    #this should add to the individual note tables
    for i in xrange(10):
        print "insertion " + str(i)
        print  "INSERT INTO note_" + str(count) + " VALUES('" + class_list[i][0] + "','" + class_list[i][1] + "'," + str(i + 1) + ",'' )"
        command = "INSERT INTO note_" + str(count) + " VALUES('" + class_list[i][0] + "','" + class_list[i][1] + "'," + str(i + 1) + ",0 )"
        c.execute(command)
        
        db.commit()
        

    print "added to small"




def retrieve_absences( user_id ):
    f="absence_sys.db"
    db = sqlite3.connect(f) 
    c = db.cursor()
    
    command = "SELECT * FROM absent_notes WHERE student_id = " + str(user_id) + ""
    c.execute(command)

    results = c.fetchall()
    ##results[x] is the xth entry
    ##results[x][y] is the yth column of the xth entry

    return results


    
