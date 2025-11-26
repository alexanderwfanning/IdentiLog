# IdentiLog
## What is it?
### Identiy Access Management (IAM) using locally stored encrypted databases using SQLCipher.
## Why are you making this?

The purpose of this project is to gain experience with "full-stack" development. This is the first proper program I have written so there are bound to be a lot of mistakes and suboptimal ways to go about things. I am attempting to create everything from scratch to demonstrate and development my understanding of fundamental concepts.

## What will it eventually be?
By the end of development, this should be a simple "authentication middleware" replacement with a focus on privacy/security. The idea is as follows:
User is met with a login page -> Attempts login -> data is queried against an encrypted locally stored database, if validated the user is redirected to the target URL of your choice. Admins have user dashboard that can see user logs.

## What is it right now?
Right now it's a login/register page with a user dashboard

## How to set up the .env file
Here is a list of environment variables necessary for operation

```
# Name of your DB
USER_DB='yourdbname.db'

# Whether or not you will have to 
REQUIRE_COMMIT='False'

# This key is only ever used internally and should be very complex.
DB_KEY='alnum_key' # 

# Admin account is automatically made when a new database is initialized. Change these and sign in with them
ADMIN_USERNAME='admin'

# This password is currently plaintext in .env but will be hashed in the DB file. This will eventually be a hashed password
ADMIN_PASSWORD='password'

# This key is used to encrypt session cookies. Make it something very complex.
FLASK_SECRET_KEY='flask_key'

# URL that a user is directed to after login. Changing this doesn't do anything yet.
REDIRECT_URL='https://URLToRedirectToAfterLogin.com/'

# Also doesn't do anything yet, but will eventually be the maximuma amount of attempts a user can try on a given account before that account is locked out until email confirmation
MAX_ATTEMPTS=''

# This is known as the "Organization Key". This is what new users will have to enter to sign up through the portal.
NEW_USER_PASSWORD='org_key'

# This will be the text that shows up on the login page and dashboard
ORGANIZATION='Organization'

```

# How to set up development environment:
## 1.
### Copy change .env.example to .env and edit the values
## 2.
### Run the following commands:

```
sudo apt-get update
pip install --upgrade pip
mkdir /identilog
cd /identilog
python -m venv .venv
source .venv/bin/activate
sudo apt-get install -y libsqlcipher-dev
pip install -r requirements.txt
flask --app pages run --debug
```