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
    command = "SELECT type FROM users WHERE email = '" + email + "' AND password = '" + password + "'"
    c.execute(command)
    results = c.fetchall()
    if (len(results) > 1):
        print "THERE ARE TWO IDENTICAL ACCOUNT LOGINS. INTERNAL ERROR"
        return False
    if (len(results) == 0):
        print "INCORRECT LOGIN"
        return False
    return True, results[0][0]
    

#add to big notes db
#create individual note db
def new_note( id, osis, student_id, parent_id, explanation, signed_by_student, signed_by_parent, date, completed):


    command = "CREATE TABLE note_" + str(id) + "( course_code INTEGER, teacher TEXT, period INTEGER, signed INTEGER )"
    pass
    
