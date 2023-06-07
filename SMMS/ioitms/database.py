import sqlite3
def create_db():
    conn=sqlite3.connect(database=r'ioitms.db')
    cur=conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS Employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text, email text, gender text, contact text, dob text, doj text, password text, usertype text, address text, salary text)")
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text, contact text, desc text)")
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Products(pid INTEGER PRIMARY KEY AUTOINCREMENT,category text, supplier text, name text, price text, quantity text, availability text)")
    conn.commit()
create_db()