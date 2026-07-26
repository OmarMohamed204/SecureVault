import sqlite3
import bcrypt

def register():
    username = input("Username: ")
    password = input("Master Password: ")

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, master_password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        print("Account created successfully!")
    
    except sqlite3.IntegrityError:
        print("Username already exists!")
    
    conn.close()

def login():
    
    username = input("Username: ")
    password = input("Master Password: ")

    conn = sqlite3.connect("passwords.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    if user and bcrypt.checkpw(
        password.encode("utf-8"),
        user[2]
    ):
        print("Login Successful!")
        conn.close()
        return user[0]
        
    
    else:
        print("Invalid username or password!")
        conn.close()
        return None