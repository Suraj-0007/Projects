import sqlite3

# Connect to the database
conn = sqlite3.connect("mistakes.db")
cursor = conn.cursor()

# Fetch and print all rows
cursor.execute("SELECT * FROM mistakes")
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}")
    print(f"User Input: {row[1]}")
    print(f"Correct Text: {row[2]}")
    print(f"Feedback: {row[3]}")
    print("-" * 40)

conn.close()
