# It's Just a Story by Carrots
# Roster
Mottaqi Abedin (PM), Jason Chan, Thomas Mackey, Yuhang Pan
# Description
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
