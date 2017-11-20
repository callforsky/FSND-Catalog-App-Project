# Shoe Catalog Web Application - A Udacity FSND Nanodegree Project
======

### Background
This project provides a list of shoe items within a variety of categories as well as provide a user registration and authentication system. Authorized users will have the ability to post, edit and delete the categories or items. This application is built with Flask and Bootstrap, thereby offering API Endpoints for the users to perform CRUD operations.

### How to Use
1. Install Vagrant and Virtual Box
2. Clone this repo
3. Go to [Google Dev website](https://console.developers.google.com) and login with your Google account
4. Go to Credentials using the left navigation panel
5. Click **Create credentials** and then **OAuth client ID**, choose **Web application**
6. Give it a name that you like and add http://localhost:5000 to your **Authorized JavaScript origins**
7. Add http://localhost:5000/login, http://localhost:5000/gconnect, https://example.com/oauth2callback, http://localhost:5000/callback to your **Authorized redirect URIs**
8. Download the JSON file and rename it to client_secrets.json
9. Use your client_secrets.json to overwrite the client_secrets.json file in this repo
10. Copy your **Client ID** from the Google Dev Console and paste it after the `data-clientid` in `login.html` (in templates folder)
11. In the terminal, `cd /catalog`
12. Launch the Vagrant VM by running `vagrant up` and then `vagrant ssh` to log in
13. Access stored files in the VM by running `cd /vagrant`
14. Set up database: `python database_setup.py`
15. Create a dummy database: `python initiate_database.py`
16. Run the web app: `python application.py`
17. In the browser, navigate to http://localhost:5000/shoecatalog
