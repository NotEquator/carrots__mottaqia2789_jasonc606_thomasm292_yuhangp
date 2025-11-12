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
c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT NOT NULL COLLATE NOCASE, bio TEXT, password TEXT NOT NULL, UNIQUE(name))")	# creates table
c.execute("CREATE TABLE IF NOT EXISTS stories (story_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, last_update DATE, author_name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS edits (edit_id INTEGER PRIMARY KEY AUTOINCREMENT, story_id INTEGER, author_name TEXT, content TEXT)")

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/", methods=['GET', 'POST'])
def index():
    # stored active session, take user to response page
    if 'username' in session:
        return redirect(url_for("home"))

    # no active session, user is taken to login
    return redirect(url_for("login"))

# Register
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # reload page if no username or password was entered
        if not username or not password:
            return render_template("register.html", error="No username or password inputted")

        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        # check if username already exists and reload page if it does
        exists = c.execute("SELECT 1 FROM users WHERE name = ?", (username,)).fetchone()
        if exists:
            db.close()
            return render_template("register.html", error="Username already exists")

        c.execute("INSERT INTO users (name, bio, password) VALUES (?, ?, ?)", (username, "temp bio", password))
        db.commit()
        db.close()

        session['username'] = username
        return redirect(url_for("home"))
    return render_template("register.html")

# GET is used to retrieve root page, removing POST or having it in does not impact the running of the page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # store username and password as a variable
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # render login page if username or password box is empty
        if not username or not password:
            return render_template('login.html', error="No username or password inputted")

        #search user table for password from a certain username
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        account = c.execute("SELECT password FROM users WHERE name = ?", (username,)).fetchone()
        db.close()

        #if there is no account then reload page
        if account is None:
            return render_template("login.html", error="Username or password is incorrect")

        # check if password is correct, if not then reload page
        if account[0] != password:
            return render_template("login.html", error="Username or password is incorrect")

        # if password is correct redirect home
        session["username"] = username
        return redirect(url_for("home"))

    return render_template('login.html')

# If 'POST' is used as the method in the html file, then 'GET' does not need to be used
@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    db_bio = c.execute("SELECT bio FROM users WHERE name=?", (session['username'],)).fetchone()
    db_editlog = c.execute("SELECT * FROM edits WHERE author_name=?", (session['username'],)).fetchall()
    stories = []
    for edit in db_editlog:
        story = c.execute("SELECT title FROM stories WHERE story_id=?", (edit[1],)).fetchone() # edit[1] = db_editlog[k][1] = story_id
        stories.append([edit[1], story[0]])  # story[0] = title
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

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    prevbio = c.execute("SELECT bio FROM users WHERE name=?", (session['username'],)).fetchone()
    if request.method == 'POST':
        newbio = request.form.get('newbio').strip()
        c.execute("UPDATE users SET bio=? WHERE name=?", (newbio, session['username'],))
        db.commit()
        db.close()

        return redirect(url_for('home'))

    return render_template('edit_profile.html',
                            prevbio = prevbio[0] if prevbio is not None else "no bio")


@app.route("/catalog")
def catalog():
    if 'username' not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    stories = []
    db_catalog = c.execute("SELECT * FROM stories").fetchall()
    for i in db_catalog:
        title = i[1]
        author = i[4]
        id = i[0]
        stories.append([id, title, author])
    db.close()
    return render_template('catalog.html',
                            stories = stories,
                            request = request.method)

@app.route("/create", methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
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
        c.execute("INSERT INTO edits (story_id, author_name, content) VALUES (?, ?, ?)", (c.lastrowid, author, content))
        db.commit()
        db.close()
        return redirect(url_for('home'))

    return render_template('create.html')

@app.route("/story/<int:story_id>")
def story(story_id):
    if 'username' not in session:
        return redirect(url_for('login'))
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
    if 'username' not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    prevcontent = c.execute("SELECT content FROM edits WHERE story_id=? ORDER BY edit_id DESC", (story_id,)).fetchone()[0]
    prevtitle, allcontent = c.execute("SELECT title, content FROM stories WHERE story_id=?", (story_id,)).fetchone()
    edit = c.execute("SELECT story_id FROM edits WHERE author_name=?", (session['username'],)).fetchall()
    has_edited = False
    for e in edit:
        if e[0] == story_id:
            has_edited = True
            break

    if request.method == 'POST':
        if not has_edited:
            content = request.form.get('content').strip()
            author = session['username']

            if not content:
                db.close()
                return render_template('edit.html', story_id=story_id, prevtitle=prevtitle, prevcontent=prevcontent)

            c.execute("UPDATE stories SET content=?, last_update=? WHERE story_id=?", (allcontent + content, datetime.datetime.now(), story_id))
            c.execute("INSERT INTO edits (story_id, author_name, content) VALUES (?, ?, ?)", (story_id, author, content))
            db.commit()
            db.close()
        return redirect(url_for('story', story_id=story_id))

    db.close()

    return render_template('edit.html', prevtitle=prevtitle, prevcontent=prevcontent, story_id=story_id, has_edited=has_edited)


@app.route("/logout")
def logout():
    session.pop('username', None) # remove username from session
    return redirect(url_for('login'))


if __name__=='__main__':
    app.debug = True
    app.run()
