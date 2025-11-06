from sqlcipher3 import dbapi2 as sqlite3
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import os, logging, getpass

#username: str, pass_hash: str, first_name: str, last_name: str, email: str
def new_user():
    print('\n --[NEW USER]--')
    username = input('Username:')
    password = getpass.getpass(prompt='Password:')
    first_name = input('First Name:')
    last_name = input('Last Name:')
    email = input('Email:')
    logging.info(f"Creating new user '{username}...'")
    pass_hash = generate_password_hash(password, method='scrypt', salt_length=16)
    cursor.execute(f"INSERT INTO users (username, pass_hash, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)", (username,pass_hash,first_name,last_name,email,))

#username: str, password: str, first_name: str, last_name: str, email: str, admin: bool
def verify_user():
    while True:
        print('\n--[LOGIN]--')

        username = input('Username:')
        password = getpass.getpass(prompt='Password:')
        cursor.execute('SELECT pass_hash from users where username = ?', (username,))
        selection = cursor.fetchone()

        if selection:
            selected_hash = selection[0] # SQLite returns a tuple, we grab the first element of the tuple so that we use it as a string in check_password_hash()
            auth = check_password_hash(selected_hash, password)
            if auth:
                print(f'User {username} successfully authenticated!')
            else:
                print("Incorrect password")
                continue
            break
        else:
            print('Username not found')
            continue




def connect():
    try:
        if new_db == False:
            logging.info(f"Connecting to {Config.user_db}...")
        else:
            logging.info(f"No database under the name '{Config.user_db}' found. Creating new database...")
        conn = sqlite3.connect(Config.user_db)

        if Config.require_commit == 'False':
            logging.info("Autocommit mode is ON. To turn it off change 'REQUIRE_COMMIT' to 'True'")
            conn.isolation_level = None
        else:
            logging.warning("Autocommit mode is OFF. NOT RECOMMENDED. To turn it on change 'REQUIRE_COMMIT' to 'False'")

        global cursor 
        cursor = conn.cursor()
        logging.info("Attempting key...")
        cursor.execute(f"PRAGMA key={Config.db_key}")


        if new_db:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (uid INTEGER, username TEXT, pass_hash TEXT, first_name TEXT, last_name TEXT, email TEXT,admin INTEGER)")
            cursor.execute(f"INSERT INTO users (uid, username, pass_hash) VALUES (1, '{Config.admin_username}', '{Config.admin_password}')")
            new_user()
            verify_user()
        else:
            verify_user()

    except sqlite3.DatabaseError as e:
        logging.critical(f"Critical Error!: {e}")
        if new_db:
            logging.critical(f"Destroying database '{Config.user_db}'")
            os.remove(Config.user_db)
        


if __name__ == "__main__":
    global new_db # Bool
    logging.basicConfig(level=logging.INFO, format='(%(asctime)s) IdentiLog %(levelname)s: %(message)s')
    try:
        logging.info("Loading configuration from .env file...")
        Config = Config()
    except Exception as e:
        logging.critical(f'Error loading config: {e}')
        exit()
    logging.info("Checking for existing database...")
    if os.path.exists('./'+ Config.user_db):
        new_db = False
        connect()
    else:
        new_db = True
        connect()