# import sqltie
import sqlite3

status=False
# Create database and connection
db=sqlite3.connect('app.db',check_same_thread=False)
print('database connected')

# cursor
cur = db.cursor()

