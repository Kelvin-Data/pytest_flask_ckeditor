import sqlite3

conn = sqlite3.connect('flask_ckeditor/message.db')

c = conn.cursor()

c.execute("""CREATE TABLE message (
    id integer primary key,
    name text,
    email text,
    subscribe boolean,
    message text
    )""")

conn.commit()

conn.close()
