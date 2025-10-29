# Mottaqi Abedin (PM), Jason Chan, Thomas Mackey, Yuhang Pan
# It's Just a Story by Carrots
# SoftDev
# P00 - Move Slowly and Fix Things
# 2025-10-28

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#create tables if it isn't there already
c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT NOT NULL, bio TEXT, password TEXT NOT NULL, UNIQUE(name))")	# creates table
c.execute("CREATE TABLE IF NOT EXISTS stories (story_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, last_update DATE, author_id INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS edits (user_id INTEGER, name TEXT)")

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/", methods=['GET', 'POST'])
def index():
    # stored active session, take user to response page
    if 'username' in session:
        return redirect(url_for("home"))

    # no active session, user is taken to login
    return redirect(url_for("login"))
# GET is used to retrieve root page, removing POST or having it in does not impact the running of the page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # store username and password as a variable
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # render login page if username or password box is empty
        if not username or not password:
            return render_template('login.html')

        session['username'] = request.form['username'] # store input in session
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
        c.execute("INSERT OR IGNORE INTO users (name, bio, password) VALUES (?, ?, ?)", (username, 'temp_bio', password)) # store user info in db
        db.commit()
        db.close()
        return redirect(url_for('index')) # process login
    return render_template('login.html')

# If 'POST' is used as the method in the html file, then 'GET' does not need to be used
@app.route("/home", methods=['GET', 'POST'])
def home():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #bio = c.execute(f"SELECT bio FROM users WHERE name={session['username']}").fetchone()[0]
    #stories = c.execute(f"SELECT story_id FROM edits WHERE name={session['username']}").fetchall()
    return render_template('home.html',
                           username=session['username'],
                           bio="temp bio",
                           stories={"story1": ["story1", "url1"],
                                    "story2": ["story2", "url2"]},
                           request=request.method)

@app.route("/logout")
def logout():
    session.pop('username', None) # remove username from session
    return render_template('logout.html')


if __name__=='__main__':
    app.debug = True
    app.run()
