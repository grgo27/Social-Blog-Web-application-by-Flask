import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect(r"C:\Users\Grgo\Desktop\PROGRAMIRANJE_PYTHON\FLASK\SOCIAL_BLOG\myproject\data.sqlite")

cur = con.cursor()

# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('SELECT * FROM users;'):
    print(row)

# Be sure to close the connection
con.close()