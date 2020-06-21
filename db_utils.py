import os
import sqlite3

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)

    create_db(con)

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
    cur.execute('CREATE TABLE IF NOT EXISTS login(name text, email text, password text)')
    cur.execute('CREATE TABLE IF NOT EXISTS report(image blob, description text)')
    
    con.commit()


def get_name(string):
    conn = db_connect()
    cur = conn.cursor()

    sql = "SELECT name FROM login"
    
    cur.execute(sql, string)

    name  = cur.fetchall()[0][0]
    return name


def export_db():
    con = db_connect()
    cur = con.cursor()

    cur.execute()


def insert_report(img, text):
    con = db_connect()
    cur = con.cursor()
    txt = 'Descricao da imagem'

    with open('pic.jpg', 'rb') as f: #pic.png is just the example
                                     #irl this will have to be checked for filetypes, etc
        data=f.read()

    cur.execute('''INSERT INTO report (image, description) VALUES (?,?)''', (data,txt))

    con.commit()


def edit_report(report_id=None):
    con = db_connect()
    cur = con.cursor()
    txt = 'Descricao da imagem'

    with open('pic.jpg', 'rb') as f: #pic.png is just the example
                                     #irl this will have to be checked for filetypes, etc
        data=f.read()

    cur.execute('''UPDATE report SET image=?, description=? WHERE report_id=?''', (data,txt, report_id))

    con.commit()

def display_image_report(report_id=None):
    m = cur.execute('select * from report WHERE report_id=?', report_id)
    for x in m:
        x[0]
        
    return x[0]
