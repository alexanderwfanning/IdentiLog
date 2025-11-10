# IdentiLog
## What is it?
### Identiy Access Management (IAM) using locally stored encrypted databases using SQLCipher.
## Why are you making this?

The purpose of this project is to gain experience with "full-stack" development. This is the first proper program I have written so there are bound to be a lot of mistakes and suboptimal ways to go about things. I am attempting to create everything from scratch to demonstrate and development my understanding of fundamental concepts.

## What will it eventually be?
By the end of development, this should be a simple "authentication middleware" replacement with a focus on privacy/security. The idea is as follows:
User is met with a login page -> Attempts login -> data is queried against an encrypted locally stored database, if validated the user is redirected to a target URL of your choice.

## What is it right now?
Right now it's just a login/register page.

## How to set up the .env file
Here is a list of environment variables necessary for operation

```
# Place these in a file named '.env' as referenced in config.py
# 
# Name of your DB
USER_DB='yourdbname.db'

# Whether or not you will have to 
REQUIRE_COMMIT='False'

# This key is only ever used internally and should be very complex.
DB_KEY='some_secret_alnum_key' # 

# Admin account is automatically made when a new database is initialized. Change these and sign in with them
ADMIN_USERNAME='admin'

# This password is currently plaintext in .env but will be hashed in the DB file. This will eventually be a hashed password
ADMIN_PASSWORD='password'

# This key is used to encrypt session cookies. Make it something very complex.
FLASK_SECRET_KEY=''

# URL that a user is directed to after login. Changing this doesn't do anything yet.
REDIRECT_URL='https://URLToRedirectToAfterLogin.com/'

# Also doesn't do anything yet, but will eventually be the maximuma amount of attempts a user can try on a given account before that account is locked out until email confirmation
MAX_ATTEMPTS=''

# This is known as the "Organization Key". This is what new users will have to enter to sign up through the portal.
NEW_USER_PASSWORD='this_is_a_super_secret_password'

# This is the footer text at the bottom. I think I'll eventually make this into "ORGANIZATION_HEADER_TEXT" and change the footer text to be a static "Powered by IdentiLog" or something
ORGANIZATION_FOOTER_TEXT='ORGANIZATION TEXT (Update in .env file)'

```

# How to run:
```
sudo apt-get update
python3 -m pip install --upgrade pip
sudo apt-get install -y libsqlcipher-dev
pip install -r requirements.txt
flask --app pages run (optional --debug flag)
```