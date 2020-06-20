import os
import sqlite3

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)

    try:
        create_db(con)
    except (sqlite3.OperationalError):
        pass

    return con
    

def add_user(email, password, name):
    conn = db_connect()
    cur = conn.cursor()

    sql = "INSERT INTO login (email, name, password) VALUES (?, ?, ?)"
    # try:
    cur.execute(sql, (email, name, password))
    conn.commit()


def check_credentials(email, password):
    conn = db_connect()
    cur = conn.cursor()

    sql = "SELECT name FROM login WHERE email=? and password=?"
    cur.execute(sql, (email, password))
    
    return cur.fetchall()


def create_db(con):
    cur = con.cursor()
    cur.execute('CREATE TABLE login(name text, email text, password text)')
    cur.execute('CREATE TABLE report(image blob, description text)')
    
    con.commit()


def export_db():
    con = db_connect()
    cur = con.cursor()

    cur.execute()


def insert_report(img, text):
    conn = db_connect()
    cur = conn.cursor()

    sql = "INSERT INTO report SET image = ?, description = ?"

    try:
        cur.execute(sql, (img, text))
        conn.commit()
        conn.close()
    except:
        conn.rollback()

        raise RuntimeError("An error occurred...")