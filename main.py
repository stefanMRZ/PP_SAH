import sys
from PyQt5.QtWidgets import QApplication
from databaseManager import DatabaseManager
from guiWindows import LoginWindow, RegisterWindow

def main():
    # 1. Inițializăm aplicația PyQt5
    app = QApplication(sys.argv)

    # 2. Pornim conexiunea la baza de date
    db = DatabaseManager()

    # 3. Instanțiem ferestrele de start
    login_win = LoginWindow(db)
    register_win = RegisterWindow(db)

    # 4. Le conectăm între ele pentru a putea naviga înainte și înapoi
    login_win.register_window = register_win
    register_win.loginWindow = login_win

    # 5. Afișăm prima fereastră
    login_win.show()

    # 6. Menținem aplicația deschisă până când dăm X
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()