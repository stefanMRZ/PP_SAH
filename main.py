import sys
from PyQt5.QtWidgets import QApplication
from databaseManager import DatabaseManager
from guiWindows import LoginWindow, RegisterWindow

def main():
    app = QApplication(sys.argv)
    db = DatabaseManager()

    login_win = LoginWindow(db)
    register_win = RegisterWindow(db)

    login_win.register_window = register_win
    register_win.loginWindow = login_win

    login_win.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()