import sqlite3

# Path to your db.sqlite3 file
database_file = '../db.sqlite3'

# Connect to the SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Query the table names from sqlite_master
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the table names
for table in tables:
    print(table[0])

# Close the connection
conn.close()

