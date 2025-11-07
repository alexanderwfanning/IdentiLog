from sqlcipher3 import dbapi2 as sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import os, logging, re
new_db = bool(True)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) IdentiLog %(levelname)s: %(message)s', filename='identi.log')
logging.info("Checking for existing database...")

try:
    logging.info("Loading configuration from .env file...")
    Config = Config()
except Exception as e:
    logging.critical(f'Error loading config: {e}')
    exit()

def validate_fields(username: str, password: str, first_name: str, last_name: str, email: str) -> bool:
    valid_username = re.fullmatch(r"^(?!_)(?!.*_$)[a-zA-Z0-9_]{3,20}$", username)
    valid_password = re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password)
    valid_email = re.fullmatch(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email)
    valid_xname = re.compile(r"^[A-Za-z '-]+$")
    valid_first_name = re.fullmatch(valid_xname, first_name)
    valid_last_name = re.fullmatch(valid_xname, last_name)
    if not valid_username:
        return False, "Invalid username format"
    if not valid_password:
        return False, "Invalid password format"
    if not valid_email:
        return False, "Invalid email format"
    if not valid_first_name:
        return False, "Invalid name format"
    if not valid_last_name:
        return False, "Invalid name format"
    return True, "Successfully Registered"


def new_user(username: str, password: str,confirm_password: str, first_name: str, last_name: str, email: str, organization_key: str) -> bool:
    if organization_key == Config.organization_key:
        if password == confirm_password:
            select_name = cursor.execute("SELECT username from users where username = ?", (username,))
            existing_user = select_name.fetchall()
            if existing_user:
                return False, "Username taken"
            else:
                select_email = cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
                existing_email = select_email.fetchall()
                if existing_email:
                    return False, "Email already registered"
                else:
                    valid_fields, field = validate_fields(username, password, first_name, last_name, email)

                    # Where user is finally created:
                    if valid_fields:
                        logging.info(f"Creating new user '{username}...'")
                        pass_hash = generate_password_hash(password, method='scrypt', salt_length=16)
                        cursor.execute(f"INSERT INTO users (username, pass_hash, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)", (username,pass_hash,first_name,last_name,email,))
                        return True, "Successfully Registered - Please sign in"
                    else:
                        return False, field
        else:
            logging.warning("Passwords don't match")
            return False, "Passwords don't match"
    else:
        logging.warning("Invalid organization key")
        return False, "Invalid organization key"


def verify_user(username: str, password: str) -> tuple[bool, str]:
        cursor.execute('SELECT pass_hash from users where username = ?', (username,))
        selection = cursor.fetchone()
        if selection:
            selected_hash = selection[0] # SQLite returns a tuple, we grab the first element of the tuple so that we use it as a string in check_password_hash()
            auth = check_password_hash(selected_hash, password)
            if auth:
               print('\033[92m' + f'User {username} successfully authenticated!' + '\033[0m')
               return True, ""
            else:
               return False, "Invalid password"
        else:
           return False, "Invalid username"

def connect():
    if os.path.exists('./'+ Config.user_db):
        new_db = False
    else:
        new_db = True
    try:
        if new_db == False:
            logging.info(f"Connecting to {Config.user_db}...")
        else:
            logging.info(f"No database under the name '{Config.user_db}' found. Creating new database...")
        conn = sqlite3.connect(Config.user_db)

        if Config.require_commit == 'False':
            logging.info("Autocommit mode is ON.")
            conn.isolation_level = None
        else:
            logging.warning("Autocommit mode is OFF. NOT RECOMMENDED. To turn it on change 'REQUIRE_COMMIT' to 'False'")

        global cursor 
        cursor = conn.cursor()
        logging.info("Attempting DB key...")
        cursor.execute(f"PRAGMA key={Config.db_key}")
        if new_db:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (uid INTEGER, username TEXT, pass_hash TEXT, first_name TEXT, last_name TEXT, email TEXT,admin INTEGER)")
            admin_pass_hash = generate_password_hash(Config.admin_password, method='scrypt', salt_length=16)
            cursor.execute(f"INSERT INTO users (uid, username, pass_hash) VALUES (1, '{Config.admin_username}', '{admin_pass_hash}')")

    except sqlite3.DatabaseError as e:
        logging.critical(f"Critical Error!: {e}")
        if new_db:
            logging.critical(f"Destroying database '{Config.user_db}'")
            os.remove(Config.user_db)
    