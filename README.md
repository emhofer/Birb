# Birb
#### Video Demo:  https://youtu.be/UkXBzS1JsdY
#### Description:


## General

Birb is a simple Twitter clone. It provides functionality to tweet ("chirp"), search tweets ("chrips") and users, follow and unfollow users, like and dislike chirps, or delete your own chirps.

---

## Features

### User management:
Users can register with a username and password. Both of these can be changed afterwards. Login and logout functions exist. Your account and all associated data can also be deleted, this has to be confirmed in a second step and is not reversible.

### Chirping:
Chirps can be pubished as text-only via the index page. After publishing, the chirps show up in the feed on the index page as well as on your profile page. The feed on the index page also shows chirps form users you follow.

### Search:
Logged in users can enter search terms in the search bar. The search function returns all users and tweets that contain the search string.

### Following:
Logged in users can follow other users. The follow button can be found on a users profile page. Unfollowing is also possible. Followed and following users show up on the index page as well as the profile page for others to see.

### Likes:
Chirps can be like and unliked. Liked chirps show up on the index page as well as the profile page for others to see.

### Delete:
Your own chirps can be deleted. This can not be reversed.

---

## Code explanations

### styles.css:
The styles.css file is used to format custom forms for deleting the user account and for customizing the default bootstrap buttons.

### scrips.js:
This file is used to control the appearance of the delete account form and for asynchronously updating the chrip feed as well as likes and chirps on the profile page.

The code runs only if certain elements (i.e. the delete account button or the chirp feed) exist on the current page. AJAX is used for asynchronous update.

### app.py:
This is the main file implementing the flask web framework. The features mentioned above are implemented in this file via routes.

### project.db:
This is the project database. It was implemented with SQLite. It contains the accounts, chirps, follows, and likes tables. The tables are modified with statements in app.py.

### helpers.py:
This file contains the login required decorator in flask, which is used in the app.py file.

### requirements.txt:
As per the Flask documentation, this file contains the libraries used/imported in app.py.

### layout.html:
This is the basic HTML template. All other HTML files extend this template. It contains a navbar, jinja code for flashing messages and a jinja block for the body of the website.

### index.html:
This this the homepage users see after logging into the website. The greeting message also links to the user's profile page. The main content on this page is the asynchronously updated chrip feed. It also contains the list of followers and followed accounts, as well as liked chirps.

### profile.html:
This is the profile page for each account. It contains likes, followers, following, and chirps for the respective account. On your own profile, there is also an option to change your username or password, as well as an option to permanently delete your account. On other profiles there is a follow/unfollow button instead.

### search.html:
This page contains the results of search queries. It is split into users and chirps. All users/chirps containing the search term are displayed. You can like chrips on this page or go to the profile page of users you searched for.

### login.html:
This page displays the login form. The root route (/) redirects here if the user is not logged in. It takes a username and password.

### register.html:
This is the signup page. It takes a username and password, as well as a password confirmation, as input. The username can not exist yet, the password must fit the requirements, and password and confirmation must match before a user is created. Once a user is created this page redirects to the login page.

### change.html:
This page contains forms to change your username or password.

### feed.html / chirps.html / likes.html:
These pages all work in similar ways. They contain content that is updated asynchronously on other pages via AJAX.

feed.html contains all of your own and followed users' chirps, with the option to like/unlike and delete, and is used on the index page.

chirps.html contains all of the user's chirps, and is used on the profile page.

likes.html contains all of the user's likes, and is used on the index page and profile page.
