import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import os #Used for os.remove()

f="absence_sys.db"
os.remove(f) #Used During Testing to remove file at the beginning

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops


def makeTables():
    command= "CREATE TABLE users(username TEXT, password TEXT, user_id INTEGER, story_edits BLOB)"
    c.execute(command);

    #Individual stories should have an ID number
    #Users should be referred to by their ID numbers
    command= "CREATE TABLE stories(title TEXT, creator_id INTEGER, story_id INTEGER)"
    c.execute(command);

    ##command = "INSERT INTO users VALUES('a', 'a', 'a')"
    ##c.execute(command);


def newUser(uname, pword):
    command = "SELECT COUNT(*) FROM users"
    count = c.execute(command)[0][0]
    command = "INSERT INTO users VALUES(uname, pword," + str(count) + ",'NULL')"
    c.execute(command)


makeTables();
newUser("ibnul", "jahan")
newUser("name", "pass")


db.commit() #save changes
db.close()  #close database
