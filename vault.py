from cryptography.fernet import Fernet
import os
import sqlite3
import secrets
import string

print(os.path.abspath("passwords.db"))

DB_PATH = os.path.join(os.path.dirname(__file__), "passwords.db")
KEY_PATH = os.path.join(os.path.dirname(__file__), "key.key")

def load_key():
    with open(KEY_PATH, "rb") as file:
        return file.read()

key = load_key()
fernet = Fernet(key)

def add_password(user_id):
    website = input("Website: ")
    email = input("Email: ")

    choice = input("Generate password (y/n): ")
    if choice.lower() in ["y", "yes"]:
        password = generate_password()

        if password is None:
            return
        
        print(f"Generated Password: {password}")

    else:
        password = input("Password: ")

    if not check_password_strength(password):
        choice = input("Do you want to save it anyway? (y/n): ")

        if choice.lower() in ["n", "no"]:
            return

    encrypted_password = fernet.encrypt(password.encode())

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO passwords (user_id, website, email, password) VALUES(?, ?, ?, ?)",
        (user_id, website, email, encrypted_password)
    )

    conn.commit()
    conn.close()

    print("Password saved successfully!")

def view_passwords(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT website, email, password From passwords WHERE user_id = ?",
        (user_id,)
    )

    passwords = cursor.fetchall()

    conn.close()

    if not passwords:
        print("No passwords found.")
        return
    
    print("\nSaved Passwords:\n")

    for password in passwords:

        print(f"Website : {password[0]}")
        print(f"Email : {password[1]}")
        print("Password : ************")
        print("=" * 30)

def delete_password(user_id):

    website = input("Website to delete: ")

    choice = input(f"Are you sure you want to delete '{website}'? (y/n): ")

    if choice.lower() not in ["y", "yes"]:
        print("Delete cancelled.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM passwords WHERE website = ? AND user_id = ?",
        (website, user_id)
    )

    if cursor.rowcount == 0:
        print("Website not found!!")

    else:
        conn.commit()

        print(f"Password for '{website}' deleted successfully!")

    conn.close()

def search_password(user_id):

    website = input("Website to search: ")

    print("-" * 30)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT website, email, password FROM passwords WHERE user_id = ? AND website = ?",
        (user_id, website)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        print(f"Website : {user[0]}")
        print(f"Email : {user[1]}")
        print("Password : ************")

    else:
        print("Website not found!!")

    print("-" * 30)

def show_password(user_id):

    website = input("Website: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM passwords WHERE user_id = ? AND website = ?",
        (user_id, website)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        print("Website not found!")
        return

    decrypted_password = fernet.decrypt(row[0]).decode()

    print(f"\nPassword: {decrypted_password}")

def generate_password():

    characters = string.ascii_letters + string.digits + string.punctuation

    try:
        length = int(input("Password length: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if length < 8 or length > 32 :
        print("Password must be between 8 and 32 characters.")
        return
    
    password = "".join(
        secrets.choice(characters)
        for i in range(length)
    )

    return password

def check_password_strength(password):

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    if len(password) >= 8 and has_upper and has_lower and has_digit and has_symbol:
        print("Strong Password ✅")
        return True

    else:
        print("Weak Password ❌")
        return False

def update_password(user_id):
    website = input("Website to update: ")
    choice = input("Generate password (y/n): ")

    if choice.lower() in ["y", "yes"]:
        password = generate_password()

        if password is None:
            return

        print(f"Generated Password: {password}")
        check_password_strength(password)

    else:
        password = input("New Password: ")

        if not check_password_strength(password):
            choice = input("Do you want to save it anyway? (y/n): ")

            if choice.lower() in ["n", "no"]:
                return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    encrypted_password = fernet.encrypt(password.encode())

    cursor.execute(
        "UPDATE passwords SET password = ? WHERE user_id = ? AND website = ?",
        (encrypted_password, user_id, website)
    )

    if cursor.rowcount == 0:
        print("Website not found!!")

    else:
        conn.commit()
        print("Password updated successfully!")

    conn.close()

def export_passwords(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT website, email, password FROM passwords WHERE user_id = ?",
        (user_id,)
    )

    passwords = cursor.fetchall()

    conn.close()

    if not passwords:
        print("No passwords found.")
        return

    with open("passwords.txt", "w") as file:

        for password in passwords:

            decrypted_password = fernet.decrypt(password[2]).decode()

            file.write(f"Website: {password[0]}\n")
            file.write(f"Email: {password[1]}\n")
            file.write(f"Password: {decrypted_password}\n")
            file.write("=" * 30 + "\n\n")

    print("Passwords exported successfully!")
    print("Warning: passwords.txt contains your passwords in plain text.")
    print("Keep this file in a safe place.")

