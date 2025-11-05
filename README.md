# It's Just a Story by Carrots
# Roster
Mottaqi Abedin (PM), Jason Chan, Thomas Mackey, Yuhang Pan
# Description
It's Just a Story is a collaborative storytelling platform built with Flask and SQLite3 that allows users to sign up or log in to create, edit, and explore shared stories. Through the navbar, users can browse stories on the Home page, search for specific ones, or view all existing stories. Logged-in users can start new stories or contribute to existing ones from their Profile page, which displays their name, bio, and past contributions. Each story page dynamically loads content from the database and includes an edit option visible only to users who haven’t yet contributed. After submitting edits, the database updates the story’s content and records the user’s ID to prevent multiple edits per story.
# Install Guide
In order to install this website, you will need to clone the repository from Github where it resides. First, you need to open the terminal and navigate to the directory where you want to clone the repo. This can be done by using the following commands:

Move to certain directory: “cd <name of directory>”
You can use “<name>/<name>/” etc. to jump forwards.
You can also replace <name of directory> with “..” to go backwards.
See the items in your current directory: “ls”

Once you are in your desired directory, gather the SSH link of the repo from Github by clicking the green “Code” button and copying the link in the SSH tab. Clone the repo by typing in the following command:

git clone <SSH link of repo> <name of folder, name it whatever you want>

Congratulations! You have successfully installed the website.

Before you run it for the first time, make sure your computer has the Flask app installed. This is one of our key components to the website and it is required for the user to have it. If you do not have it installed, follow this guide: https://flask.palletsprojects.com/en/stable/installation/.

# Launch Codes
Navigate in the terminal to the repo folder if you haven’t already. Then, run the website using the following command:

flask --app app.py run

The terminal will say that the website is running on http://127.0.0.1:5000 (or something similar). Copy and paste that link into your browser.

Congratulations! You are ready to be an amazing storyteller!
