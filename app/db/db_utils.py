from sqlcipher3 import dbapi2 as sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.config import Config
from .fields import validate_fields
import os, logging
new_db = bool(True)
logging.basicConfig(level=logging.INFO, format='(%(asctime)s) IdentiLog %(levelname)s: %(message)s')
logging.info("Checking for existing database...")

try:
    logging.info("Loading configuration from .env file...")
    Config = Config()
except Exception as e:
    logging.critical(f'Error loading config: {e}')
    exit()

def new_user(username: str, password: str,confirm_password: str, first_name: str, last_name: str, email: str, organization_key: str) -> bool:
    info = []
    for field in [username, first_name, last_name, email]:
        field = field.strip(" ")
        field = field.lower()
        info.append(field)

    if organization_key == Config.organization_key:
        if password == confirm_password:
            select_name = cursor.execute("SELECT username from users where username = ?", (info[0],))
            existing_user = select_name.fetchall()
            if existing_user:
                return False, "Invalid username"
            else:
                select_email = cursor.execute("SELECT email FROM users WHERE email = ?", (info[3],))
                existing_email = select_email.fetchall()
                if existing_email:
                    return False, "Email already registered"
                else:
                    valid_fields, field = validate_fields(info[0], password, info[1], info[2], info[3])

                    # Where user is finally created:
                    if valid_fields:
                        logging.info(f"Creating new user '{username.lower()}...'")
                        pass_hash = generate_password_hash(password, method='scrypt', salt_length=16)
                        cursor.execute(f"INSERT INTO users (username, pass_hash, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)", (username.lower(),pass_hash,first_name.lower(),last_name.lower(),email.lower(),))
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
            cursor.execute("SELECT pass_hash FROM users WHERE username = ?", (username.lower(),))
            pass_hash = cursor.fetchone()
            selected_hash = pass_hash[0] if pass_hash else ""
            auth = check_password_hash(selected_hash, password)
            if auth:
               print('\033[92m' + f'User {username} successfully authenticated!' + '\033[0m')
               return True, ""
            else:
               return False, "Invalid credentials"

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