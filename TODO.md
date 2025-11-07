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
    - [ ] Lock attempts (environment variable)