# It's Just a Story by Carrots
# Roster
Mottaqi Abedin (PM), Jason Chan, Thomas Mackey, Yuhang Pan
# Description
 We are developing a collaborative storytelling website using a Flask web application integrated with an SQLite3 database. The platform allows users to log in or sign up to participate in a shared writing experience where they can either create new stories or add to existing ones created by other users.
 
Once logged in, users will be directed to a personalized landing page that displays their profile information (name and bio), a list of stories they have contributed to, and an option to create a new story. If a visitor is not logged in, they will instead see a simplified homepage with links to the login and registration pages.

The app uses Flask’s routing system to manage navigation between pages such as the homepage, login/register page, individual story pages, and edit or create story pages. Each story page dynamically loads content from the database, showing the latest version of the story. To maintain fairness and creativity in collaboration, each user can only edit or add to a story once — after contributing, they can view the updated version but cannot make further changes.

The site also features a consistent navigation bar across all pages, providing quick access to the homepage, a search bar to find stories by title or keyword, and a logout button.

From a technical standpoint, the application uses Flask sessions to handle authentication securely, ensuring users stay logged in across different pages. The SQLite3 database manages three main tables:
Users – stores user credentials, bios, and the stories they’ve contributed to.
Stories – stores the title, content, creation date, and last updated timestamp for each story.
Edits – links users to the stories they’ve edited, preventing multiple edits from the same account.

All pages are rendered using Jinja2 HTML templates, which dynamically display user data, story content, and interactive forms for story creation and editing. A create story page allows users to submit new stories, while an edit page provides a pre-filled text form containing the current story content so the user can make additions or modifications before saving.

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
