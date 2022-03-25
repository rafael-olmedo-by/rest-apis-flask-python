import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS books (title TEXT, authors TEXT, price REAL)'
cursor.execute(create_table)

cursor.execute("INSERT INTO books VALUES ('String Theory', 'Joseph Polchinski', 99.99)")

connection.commit()
connection.close()
