# sourJambaJuiceCandy
### Team Roster: Ibnul Jahan (PM), Caleb Smith-Salzberg, Anish Shenoy, Jasper Cheung
### Project name: absencio

*The world has never witnessed a project of this caliber* <br>
**Stuyvesant, get ready** 

**Check out our app: http://absencio.stuycs.org** <br>
**[DEMO](absencio/absencio.mp4)**

### Overview: Absencio aims to simplfy and streamline the process of absence notes. 
* ***Students***:
High schoolers will log in and use the program to submit excuse notes for days they were absent/late. This
will be done by selecting the day of the incident, and then digitally filling out the form. At the
conclusion of the filling, an email will be sent to the student’s parents’ accounts for verification
and a digital signature.
*  ***Parents***:
As a student submits a form for approval, an email automatically is sent to the parent to receive confirmation. Here, the
parent is able to open the form and see all the information the student is filled out. If deemed
accurate and acceptable, the parent may add their digital signature and confirm the form. If not, the parent can reject the student’s submission.

*  ***Teachers***:
Teacher will log in to their accounts. At the conclusion of the parent portion of the excuse note cycle, the form is sent to the respective teachers, but this time complete with parent signature. If they do accept and provide their
digital signature as proof, a copy of the form living in the student’s account is updated with the
signature.

## Launch Instructions(Locally)
### Getting Started
### Dependencies
* Python 2.7
* Flask
* Requests
* SQLite3

### Virtual Environment, Flask, and Requests
Flask needs to be installed in order to run this program. It is ideally stored in a virtual environment (venv).

To install a venv called `<name>`, run these commands in your terminal:
```
$ pip install virtualenv
$ virtualenv <name>
```
On Mac/Linux, start up your venv with:
```
$ . <name>/bin/activate
```
On Windows:
```
$ . <name>/Scripts/activate
```
In your activated venv, run the following:
```
$ pip install flask
$ pip install requests
```
### SQLite3
Download SQLite3 [here](https://www.sqlite.org/download.html).

### Launching the App (Locally)
With your virtual environment activated:
```
$ git clone https://github.com/ibnullify/sourJambaJuiceCandy.git absencio 
```
or
```
$ git clone git@github.com:ibnullify/sourJambaJuiceCandy.git absencio
```
then
```
$ cd absencio/absencio
$ python __init___.py
```
You can now view the webpage by opening the URL `localhost:5000` in Chrome, Firefox, or Safari

