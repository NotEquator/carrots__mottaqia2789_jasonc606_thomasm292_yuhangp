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
import datetime


DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

#create tables if it isn't there already
c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT NOT NULL, bio TEXT, password TEXT NOT NULL, UNIQUE(name))")	# creates table
c.execute("CREATE TABLE IF NOT EXISTS stories (story_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, last_update DATE, author_name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS edits (story_id INTEGER, author_name TEXT)")

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
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        # store username and password as a variable
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # render login page if username or password box is empty
        if not username or not password:
            db.close()
            return render_template('login.html')

        #search user db for password from a certain username
        pw_result = c.execute("SELECT password FROM users WHERE name = ?", (username,)).fetchone()

        #if there is a user with that username in the db, check if password is correct. else create a new user.
        if pw_result is not None:
            db_password = pw_result[0]
            # if password in session matches the one in db, redirect to home. else render login template
            if password == db_password:
                session['username'] = username
                db.close()
                return redirect(url_for("home"))
            else:
                db.close()
                return render_template('login.html')
        else:
            c.execute("INSERT OR IGNORE INTO users (name, bio, password) VALUES (?, ?, ?)", (username, 'temp_bio', password)) # store user info in db
            db.commit()
            db.close()
            session['username'] = username
            return redirect(url_for('home'))

    return render_template('login.html')

# If 'POST' is used as the method in the html file, then 'GET' does not need to be used
@app.route("/home", methods=['GET', 'POST'])
def home():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    db_bio = c.execute("SELECT bio FROM users WHERE name=?", (session['username'],)).fetchone()
    db_editlog = c.execute("SELECT * FROM edits WHERE author_name=?", (session['username'],)).fetchall()
    stories = []
    for edit in db_editlog:
        story = c.execute("SELECT title FROM stories WHERE story_id=?", (edit[0],)).fetchone() # edit[0] = db_editlog[k][0] = story_id
        stories.append([edit[0], story[0]])  # story[0] = title
    # db_storyid = db_editlog[0] if db_editlog else None
    # print("\n\n\n**********")
    # print(db_storyid)
    # print(db_storyid[0] if db_storyid else "No story id found")
    # db_stories = c.execute("SELECT * FROM stories WHERE story_id =?", (db_storyid[0],)).fetchone()
    # print("\n\n\ndbstories**********")
    # print(db_stories)
    db.close()
    return render_template('home.html',
                           username=session['username'],
                           bio=db_bio[0] if db_bio is not None else "no bio",
                           stories=stories,
                           request=request.method)

@app.route("/catalog")
def catalog():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    stories = []
    db_catalog = c.execute("SELECT * FROM stories").fetchall()
    for i in db_catalog:
        title = i[1]
        author = i[4]
        select_id = c.execute("SELECT story_id FROM edits WHERE story_id=?", (i[0],)).fetchone()
        id = select_id[0]
        stories.append([id, title, author])
    db.close()
    return render_template('catalog.html',
                            stories = stories,
                            request = request.method)

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        title = request.form.get('title').strip()
        content = request.form.get('content').strip()
        author = session['username']

        if not title or not content:
            db.close()
            return render_template('create.html')

        c.execute("INSERT INTO stories (title, content, last_update, author_name) VALUES (?, ?, ?, ?)", (title, content, datetime.datetime.now(), author))
        c.execute("INSERT INTO edits (story_id, author_name) VALUES (?, ?)", (c.lastrowid, author))
        db.commit()
        db.close()
        return redirect(url_for('home'))

    return render_template('create.html')

@app.route("/story/<int:story_id>")
def story(story_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    story = c.execute("SELECT title, content, last_update, author_name FROM stories WHERE story_id=?", (story_id,)).fetchone()
    edit = c.execute("SELECT story_id FROM edits WHERE author_name=?", (session['username'],)).fetchall()
    has_edited = False
    for e in edit:
        if e[0] == story_id:
            has_edited = True
            break
    db.close()

    return render_template("story.html",
                            title=story[0],
                            content=story[1],
                            last_update=story[2],
                            author=story[3],
                            story_id=story_id,
                            has_edited=has_edited
    )

@app.route("/edit/<int:story_id>", methods=['GET', 'POST'])
def edit(story_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if request.method == 'POST':
        title = request.form.get('title').strip()
        content = request.form.get('content').strip()
        author = session['username']

        if not title or not content:
            db.close()
            prevtitle, prevcontent = c.execute("SELECT title, content FROM stories WHERE story_id=?", (story_id,)).fetchone()
            return render_template('edit.html', story_id=story_id, prevtitle=prevtitle, prevcontent=prevcontent)

        c.execute("UPDATE stories SET title=?, content=?, last_update=? WHERE story_id=?", (title, content, datetime.datetime.now(), story_id))
        c.execute("INSERT INTO edits (story_id, author_name) VALUES (?, ?)", (story_id, author))
        db.commit()
        db.close()
        return redirect(url_for('story', story_id=story_id))

    prevtitle, prevcontent = c.execute("SELECT title, content FROM stories WHERE story_id=?", (story_id,)).fetchone()
    db.close()

    return render_template('edit.html', prevtitle=prevtitle, prevcontent=prevcontent, story_id=story_id)


@app.route("/logout")
def logout():
    session.pop('username', None) # remove username from session
    return render_template('logout.html')


if __name__=='__main__':
    app.debug = True
    app.run()
