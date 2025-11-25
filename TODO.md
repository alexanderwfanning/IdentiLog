#To Do

1. [**Phase 1**]

    - [x] Deploy a basic login page using Flask
    - [x] Make the login page somewhat pretty using html/css
    - [x] Create user database using PySQLCipher3
    - [x] Get a basic layout of required environment variables

2. [**Phase 2**]

    - [x] Set up password hashing system and environment variables to store admin account
    - [x] Refactor verify_user() to handle data from flask taken from form submission
    - [x] Flask (pages.py) extract form data and uses verify_user() from data.py
        * [x] Flask Routing methods=['GET', 'POST'] 
        * [x] Flask Sessions store data and how to set app.secret_key?
        * [x] Flask redirects with "redirect()" and "url_for()"
    - [x] Build registration page
    - [x] Validate fields from registration page
        * [x] Not taken
        * [x] Proper format
    - [x] Jinja2 templates for invalid login/registration attempts?
    - [x] Automatically output *system* logs to files
    - [ ] Automatically output *user* logs to separate file (XML OR JSON? so that we can make it pretty for a dashboard viewer)
    - [x] Automatically lowercase username & emails when inserting and selecting from db
    - [ ] Create dashboard page with welcome message
    - [ ] Add logout functionality
    - [ ] Update login to redirect to dashboard (not just render template)
    - [ ] Add "stay logged in" checkbox functionality
    - [ ] Test all flows work (register → login → dashboard → logout)
    - [ ] Add services list to dashboard (hardcoded for now)
    - [ ] Service name, URL
    - [ ] Display as cards/grid
    - [ ] Links open in new tab
    - [ ] Create basic admin panel page
    - [ ] Check if user is admin (add admin column check)
    - [ ] Show list of all users
    - [ ] Show user count, registration dates
    - [ ] Add navigation between pages (dashboard ↔ admin panel

3. [**Phase 3**]
    - [ ] Admin: Add ability to delete users
    - [ ] Admin: Add ability to toggle admin status
    - [ ] Admin: View user details (email, registration date, last login)
    - [ ] Add "last login" timestamp to database
    - [ ] Update last login on successful login
    - [ ] Fix error messages (don't leak username existence)
    - [ ] Add rate limiting to login endpoint
    - [ ] Add session timeout configuration
    - [ ] Improve password requirements display on register page
    - [ ] Add "confirm password" client-side validation (JavaScript)
    - [ ] Add favicon
