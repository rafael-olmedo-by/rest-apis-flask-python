import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

drop_table = 'DROP TABLE IF EXISTS users'
create_table = 'CREATE TABLE users (id int, username text, password text)'
insert_into_table = 'INSERT INTO users VALUES (?, ?, ?)'
select_table = 'SELECT * FROM users'

user = (1, 'bob', 'asdf')
users = [
    (2, 'rolf', 'abcd'),
    (3, 'lisa', 'wxyz')
]

cursor.execute(drop_table)
cursor.execute(create_table)
cursor.execute(insert_into_table, user)
cursor.executemany(insert_into_table, users)

for row in cursor.execute(select_table):
    print(row)

connection.commit()
connection.close()
