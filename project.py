from auth import register, login 
from database import create_tables
from vault import (
    add_password,
    view_passwords,
    delete_password,
    search_password,
    generate_password,
    check_password_strength,
    update_password,
    export_passwords,
    show_password
)

def main():

    create_tables()

    while True:
        print("\n===== SecureVault =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1" :
            register()
        
        elif choice == "2":
            user_id = login()
            
            if user_id:
                while True:
                    print("\n===== Password Manager =====")
                    print("1. Add Password")
                    print("2. View Passwords")
                    print("3. Search Password")
                    print("4. Show Password (Reveal)")
                    print("5. Update password")
                    print("6. Delete password")
                    print("7. Generate Password")
                    print("8. Check Password Strength")
                    print("9. Export Passwords")
                    print("10. Logout")

                    choice = input("Choose an option: ")

                    if choice == "1":
                        add_password(user_id)
                    
                    elif choice == "2":
                        view_passwords(user_id)

                    elif choice == "3":
                        search_password(user_id)

                    elif choice == "4":
                        show_password(user_id)

                    elif choice == "5":
                        update_password(user_id)
                        
                    elif choice == "6":
                        delete_password(user_id)

                    elif choice == "7":
                        password = generate_password()

                        if password:
                            print(f"Generated Password: {password}")
                            check_password_strength(password)

                    elif choice == "8":
                        password = input("Enter Password: ")
                        check_password_strength(password)
                        
                    elif choice == "9":
                        export_passwords(user_id)

                    elif choice == "10":
                        print("Logged out successfully!!")
                        break

                    else:
                        print("Invalid choice!! Try again.")


        
        elif choice == "3":
            print("Goodbye!")
            break

        else :
            print("Invalid choice!! Try again.")

if __name__ == "__main__":
    main()