import sqlite3
db=sqlite3.connect('db.db')


cursor=db.cursor()

cursor.execute("CREATE TABLE USER (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255), lastname VARCHAR(255))")