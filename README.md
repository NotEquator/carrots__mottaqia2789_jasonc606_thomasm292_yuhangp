# It's Just a Story by Carrots
# Roster
Mottaqi Abedin (PM), Jason Chan, Thomas Mackey, Yuhang Pan
# Description
It's Just a Story is a collaborative storytelling platform built with Flask and SQLite3 that allows users to sign up or log in to create, edit, and explore shared stories. Through the navbar, users can browse stories on the Home page, search for specific ones, or view all existing stories. Logged-in users can start new stories or contribute to existing ones from their Profile page, which displays their name, bio, and past contributions. Each story page dynamically loads content from the database and includes an edit option visible only to users who haven’t yet contributed. After submitting edits, the database updates the story’s content and records the user’s ID to prevent multiple edits per story.
# Install Guide
First, you will need to clone the repository from Github where it resides by typing this command into the terminal:  
`git clone git@github.com:NotEquator/carrots__mottaqia2789_jasonc606_thomasm292_yuhangp.git Its_Just_A_Story`

Next, you need to open a virtual environment:  
`python3 -m venv venv`

Then, activate that virtual environment:  
Windows: `venv\Scripts\activate`  
MacOS and Linux: `. venv/bin/activate`

Finally, install the components needed to run the website:  
`pip install -r Its_Just_A_Story/requirements.txt`

Congratulations! You have installed the website!

# Launch Codes
Launching the website is easy. Just run this command:  
`python Its_Just_A_Story/app/__init__.py`

On your broswer enter this URL:  
`http://127.0.0.1:5000`

Congratulations! You are ready to be an amazing storyteller!
