#!usr/bin/python

import os, sys, sqlite3

f="absence_sys.db"
db = sqlite3.connect(f)
c = db.cursor()    

#creating the db is handled in ../db_builder.py

def activateable( email, activation_code ) :
    f="absence_sys.db"
    db = sqlite3.connect(f) 
    c = db.cursor() 
    command = "SELECT * FROM users WHERE email = '" + email + "'"
    c.execute(command);
    results = c.fetchall()
    ##results[x] is the xth entry
    ##results[x][y] is the yth column of the xth entry
    print results, len(results), results[0], results[0][0]
    if (len(results) > 1):
        print "THERE EXISTS MORE THAN ONE ACCOUNT WITH THAT EMAIL. INTERNAL ERROR!"
        return False
    if (len(results) == 0):
        print "THAT EMAIL IS NOT ASSOCIATED WITH AN ACCOUNT!"
        return False
    return True

##how do you update entries
def activate_account( username, newpass ):
    f="absence_sys.db"
    db = sqlite3.connect(f) 
    c = db.cursor() 
    #command = "SELECT password FROM users WHERE email = '" + email + "'"
    command = "UPDATE users SET password = '" + newpass + "' WHERE username = '" + username + "'"
    c.execute(command);
    print c.fetchall()
    #results = c.fetchall()
    print "password updated"

def check_account( email, password ):
    pass
