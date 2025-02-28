import sqlite3

# Connect to database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Insert valid users
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'userpass')")

# Insert a vulnerable entry (For SQL Injection Exploit)
cursor.execute("INSERT INTO users (username, password) VALUES ('admin-sqli', 'fakepassword')")

# Save & close
conn.commit()
conn.close()

print("✅ Database setup completed!")
