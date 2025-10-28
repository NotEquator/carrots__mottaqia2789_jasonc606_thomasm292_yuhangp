# names
# It's Just a Story by Carrots
# SoftDev
# P00 - Move Slowly and Fix Things
# 2025-10-28

from flask import Flask           
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def landing_page():
    if 'username' in session:
        return redirect(url_for("index"))
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.debug = True
    app.run()
