import os
import sqlite3

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS login(user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT, email TEXT, password TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS report(report_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, image blob, description text)')

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
    
    with open(img, 'rb') as f: 
        data=f.read()

    cur.execute('''INSERT INTO report (image, description) VALUES (?,?)''', (data,text))

    con.commit()


def edit_report(report_id, txt):
    con = db_connect()
    cur = con.cursor()

    try:
        cur.execute('SELECT image FROM report WHERE report_id=?', (report_id))
    except:
        pass
    rows = cur.fetchall
    cur.execute('''UPDATE report SET image=?, description=? WHERE report_id=?''', (data,txt, report_id))

    con.commit()

def display_image_report(report_id):
    con = db_connect()
    cur = con.cursor()
    try:
        m = cur.execute('select * from report WHERE report_id=?', str(report_id))
    except:
         con.close()
         print('Algo de errado aconteceu')

    for x in m:
        rec_data = x[1]
        
    with open(str(report_id), 'wb') as fw:
        fw.write(rec_data)

def report_table_size():
    con = db_connect()
    cur = con.cursor()
    cur.execute('select report_id from report')
    rows = cur.fetchall()

    return len(rows)


def report_list():
    con = db.connect()
    cur = con.cursor()

    cur.execute()
