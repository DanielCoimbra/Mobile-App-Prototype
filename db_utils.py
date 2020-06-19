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


def insert_login(login, password):
    conn = db_connect()
    cur = conn.cursor()

    sql = "INSERT INTO login (user, password) VALUES (?, ?)"
    # try:
    cur.execute(sql, (login, password))
    conn.commit()
        
    # except:
    #     conn.rollback()
    #     raise RuntimeError("An error occurred...")

def check_login(login, password):
    conn = db_connect()
    cur = conn.cursor()

    sql = "SELECT user, password FROM login WHERE user='ADMIN', password='ADMIN'"

          
    try:
        cur.execute(sql)
        
    print(cur.fetchall()[0])
    conn.commit()


def create_db(con):
    cur = con.cursor()
    cur.execute('CREATE TABLE login(user text, password text)')
    cur.execute('CREATE TABLE report(image blob, description text)')
    
    con.commit()
    
    con.close()

def export_db():
    con = db_connect()
    cur = con.cursor()

    cur.execute()



def formulario(text):

    import sqlite3
    con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db.sqlite3'))
    cur = con.cursor()
    try:
        cur.execute('CREATE TABLE formulario(texto text)')
    except sqlite3.OperationalError:
        pass
    cur.execute('INSERTO INTO formulario (texto) VALUES (?)', self.text.text)
    con.commit()
    con.close()
