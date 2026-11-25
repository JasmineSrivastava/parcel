from database import db_setup
from menus import customer_menu, officer_menu
from services import auth_service


def main():
    conn, cur = db_setup.get_connection() #connection banarahe isse

    print("Database connection established successfully.")

    db_setup.init_db(cur)  #ab yaha query run karenge


    print("=========================================")
    print("      PARCEL MANAGEMENT SYSTEM  ")
    print("=========================================")
    while True:
        print("\n1. User Registration\n2. Log in\n3. Exit")
        option = input("Enter option: ").strip()
        if option == "1":
            auth_service.register_user(cur)
        elif option == "2":
            user = auth_service.login_user(cur)
            if user:
                if user.role == "Officer":
                    officer_menu.run(cur, user)
                else:
                    customer_menu.run(cur, user)
        elif option == "3":
            print("Thank you for using the Parcel Management System. Goodbye! 😊")
            break
        else:
            print("  [Error] Invalid option. Please enter 1, 2 or 3.")
    conn.close()


if __name__ == "__main__":
    main()
