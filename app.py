# -*- coding: utf-8 -*-

'''
In this example, we are going to creat a *very simple* webapp.
# Local Preview
At the command line: 
set FLASK_ENV=development (once per session)
flask run  (each time run the app)
'''

# request: a flask object 
# interation with app, eg user input 
from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)  # __name__: name of the file 

# g imported from flask, stands for global, name space var
def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect('messages_db.sqlite')
    
    g.message_db.execute("CREATE TABLE IF NOT EXISTS messages (ID integer, NAME varchar, message varchar);")
    return g.message_db

def insert_message(request):
    message = request.form["message"]
    name    = request.form["name"]
    db = get_message_db()
    ID = 1 + db.execute("SELECT COUNT(*) FROM messages;").fetchone()[0]
    db.execute("INSERT INTO messages (ID, NAME, message) VALUES (?, ?, ?);", (ID, name, message))
    db.commit()
    db.close()

def random_messages(n):
	db = get_message_db()
	entries = db.execute('SELECT NAME, message FROM messages ORDER BY RANDOM() LIMIT ?;', [n]).fetchall()
	db.close()
	return entries

@app.route("/", methods=['POST', 'GET'])  # the first thing the user sees when nagivate to the page
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        insert_message(request)
        return render_template('submit.html', thanks = True)


@app.route("/view/")
def view():
	entries = random_messages(5)
	return render_template("view.html", entries = entries)