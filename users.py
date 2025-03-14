import sqlite3
import subprocess
import os

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL UNIQUE,
        score INTEGER DEFAULT 0
    )''')
conn.commit()
conn.close()

def register():
    username = input("enter username: ")
    password = input("enter password: ")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    print("Registration successful")

def login():
    username = input("enter username: ")
    password = input("enter password: ")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result is not None and result[0] == password:
        print("logged in")
        return username 
    else:
        print("login failed")
        return False

def update_score(username, new_score):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET score = score + ? WHERE username = ?", (new_score, username))
    conn.commit()
    conn.close()
    print("Score updated")

def main_menu():
    while True:
        print("1. Registrovat")
        print("2. Prihlasit se")
        print("3. Odejit")
        print("4. Žerbříček")
        choice = input("Vyber volbu: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                env = os.environ.copy()
                env["USERNAME"] = user 
                subprocess.run(["python3", "sibenice.py"], env=env)
        elif choice == "3":
            break
        elif choice == "4":
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 10")
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                print(row[0], row[1])
                print("")
        else:
            print("Neplatna volba, zkuste znovu.")

if __name__ == "__main__":
    main_menu()