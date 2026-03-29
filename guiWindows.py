import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from databaseManager import DatabaseManager

class BaseWindow(QWidget):
    def __init__(self, title = "Sah Player2Player", width = 900, height = 750):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(width, height)
        self.centerWindow()

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showMessage(self, title, text, isError = False):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)

        if isError:
            msg.setIcon(QMessageBox.Warning)
        else:
            msg.setIcon(QMessageBox.Information)

        msg.exec_()

    def setupUi(self):
        pass

class LoginWindow(BaseWindow):
    def __init__(self, dbManager):
        super().__init__(title="Login - Sah Player2Player", width=900, height=750)
        self.dbManager = dbManager
        self.register_window = None
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()

        self.label = QLabel("Conectare Jucator")

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Nume Utilizator")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Parola Utilizator")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.handleLogin)

        self.btn_go_register = QPushButton("Nu ai cont? Inregistreaza-te")
        self.btn_go_register.clicked.connect(self.go_to_register)

        layout.addWidget(self.label)
        layout.addWidget(self.input_user)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_go_register)

        self.setLayout(layout)

    def handleLogin(self):
        user = self.input_user.text()
        passwd = self.input_password.text()

        if not user or not passwd:
            self.showMessage("Eroare","completati ambele campuri!", is_error=True)
            return

        if self.dbManager.loginUser(user, passwd):
            self.showMessage("Succes","Autentificare realizata cu succes!")
        else:
            self.showMessage("Eroare","Username sau parola gresita, inregistrati utilizatorul...", isError=True)
            self.go_to_register()

    def go_to_register(self):
        if self.register_window:
            self.hide()
            self.register_window.show()

class RegisterWindow(BaseWindow):
    def __init__(self, dbManager):
        super().__init__(title="Inregistrare Sah Player2Player", width=900, height=750)
        self.dbManager = dbManager
        self.loginWindow = None
        self.setupUi()

    def setupUi(self):
        Layout = QVBoxLayout()

        self.label = QLabel("Creare cont nou")
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Nume Utilizator")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Parola Utilizator")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_register = QPushButton("Inregistreaza")
        self.btn_register.clicked.connect(self.handleRegister)

        self.btn_go_login = QPushButton("Ai deja cont. Mergi la Login")
        self.btn_go_login.clicked.connect(self.go_to_login)

        Layout.addWidget(self.label)
        Layout.addWidget(self.input_user)
        Layout.addWidget(self.input_password)
        Layout.addWidget(self.btn_register)
        Layout.addWidget(self.btn_go_login)

        self.setLayout(Layout)

    def handleRegister(self):
        user = self.input_user.text()
        passwd = self.input_password.text()

        if not user or not passwd:
            self.showMessage("Eroare","completati ambele campuri!", is_error=True)
            return

        if self.dbManager.registerUser(user, passwd):
            self.showMessage("Succes","Cont creat. Redirectionam la Login!")
            self.go_to_login()
        else:
            self.showMessage("Eroare","Username existent, mergi la login", isError=True)
            self.go_to_login()

    def go_to_login(self):
        if self.loginWindow:
            self.hide()
            self.loginWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    db = DatabaseManager()

    login_win = LoginWindow(db)
    register_win = RegisterWindow(db)

    login_win.register_window = register_win
    # Corectat aici: loginWindow (cu W mare) in loc de login_window
    register_win.loginWindow = login_win

    login_win.show()

    sys.exit(app.exec_())
