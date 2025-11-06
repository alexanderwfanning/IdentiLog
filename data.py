from sqlcipher3 import dbapi2 as sqlite3
from config import Config
import os, logging

def verify_user():
    pass

def main():
    try:
        logging.info("Checking for existing database...")
        if os.path.exists('./'+ Config.user_db):
            new_db = False
            logging.info(f"Connecting to {Config.user_db}...")
        else:
            new_db = True
            logging.info(f"No database under the name '{Config.user_db}' found. Creating new database...")
        conn = sqlite3.connect(Config.user_db)
        if Config.require_commit == 'False':
            logging.info("Autocommit mode is ON. To turn it off change 'REQUIRE_COMMIT' to 'True'")
            conn.isolation_level = None
        else:
            logging.info("Autocommit mode is OFF. To turn it on change 'REQUIRE_COMMIT' to 'False'")
        cursor = conn.cursor()
        logging.info("Attempting key...")
        cursor.execute(f"PRAGMA key={Config.db_key}")
        if new_db:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (uid INTEGER, username TEXT, pass_hash TEXT, first_name TEXT, last_name TEXT, email TEXT,admin INTEGER)")
            cursor.execute("INSERT INTO users (uid, first_name, last_name, email, admin) VALUES (1, 'Admin', 'Xander', 'adminxander@xanlab.net', 1) ")
        admin_users = cursor.execute("SELECT first_name, last_name FROM users WHERE admin=1").fetchall()
    except sqlite3.DatabaseError as e:
        logging.critical(f"Critical Error!: {e}")
        if new_db:
            logging.critical(f"Destroying database '{Config.user_db}'")
            os.remove(Config.user_db)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='(%(asctime)s) IdentiLog %(levelname)s: %(message)s')
    try:
        Config = Config()
    except Exception as e:
        logging.critical(f'Error loading config: {e}')
        exit()
    main()