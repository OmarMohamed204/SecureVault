# SecureVault

## Description

SecureVault is a command-line password manager developed in Python as my CS50 Final Project.

The purpose of this project is to provide users with a simple and secure way to manage their passwords without relying on online password managers. Users can create an account, log in securely, save passwords for different websites, update them, search for them, delete them, and export them when needed.

Security was the main focus during the development of this project. User login passwords are never stored as plain text. Instead, they are hashed using the bcrypt library before being saved in the SQLite database. This means that even if someone gains access to the database, the original login passwords cannot be recovered.

Website passwords are handled differently. Since the application needs to display them again when the user requests them, they are encrypted using the Fernet implementation provided by the cryptography library. Unlike hashing, encryption allows the original password to be decrypted only by using the secret encryption key stored in the key.key file.

The application also includes a password generator that creates strong random passwords using uppercase letters, lowercase letters, numbers, and special characters. Users can also check the strength of any password before saving it.

For additional safety, passwords are hidden when viewing saved accounts. If the user wants to reveal a password, they must explicitly choose the "Show Password" option. Before deleting a password, the application also asks for confirmation to prevent accidental deletion.

Another useful feature is exporting all saved passwords into a text file. Since exported passwords are stored in plain text, the program displays a warning reminding the user to keep the file in a safe place.

The project uses SQLite as its database because it is lightweight, portable, and does not require a separate database server. The project is divided into multiple Python modules to improve readability and maintainability.

## Features

- User registration
- Secure login with bcrypt hashing
- Store website credentials
- Encrypt passwords using Fernet
- Generate strong passwords
- Check password strength
- Search passwords
- Update passwords
- Delete passwords with confirmation
- Hide saved passwords
- Reveal passwords only when requested
- Export passwords to a text file

## Files

### project.py
Contains the main menu and controls the application flow.

### auth.py
Handles user registration and login.

### vault.py
Implements all password management operations.

### database.py
Creates the SQLite database and its tables.

### generator.py
Generates the Fernet encryption key.

### passwords.db
Stores users and encrypted passwords.

### key.key
Stores the encryption key used by Fernet.

### requirements.txt
Contains the required external Python libraries.

## Libraries

- bcrypt
- cryptography

## Design Choices

One important design decision was using two different methods to protect passwords.

The master password used for logging in is hashed with bcrypt because it never needs to be recovered. Hashing provides stronger protection than encryption for authentication.

Website passwords, however, must be shown to the user later. Because of that, they are encrypted using Fernet instead of being hashed. This allows the application to decrypt them only when the user explicitly requests to reveal a password.

I also separated the project into multiple files instead of writing everything in one script. This makes the project easier to understand, maintain, and extend in the future.