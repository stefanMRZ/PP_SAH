import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QSizePolicy
from databaseManager import DatabaseManager
from ipcManager import ipcManager
from chessLogic import Board

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
            self.lobby_window = LobbyWindow(self.dbManager, user)
            self.hide()
            self.lobby_window.show()
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

class LobbyWindow(BaseWindow):
    def __init__(self, dbManager, username):
        super().__init__(title="Lobby - Sah Player2Player", width=900, height=750)
        self.dbManager = dbManager
        self.username = username
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()

        self.label = QLabel("Conectare realizata. Alege actiune")

        self.input_search_user = QLineEdit()
        self.input_search_user.setPlaceholderText("Nume Utilizator")

        self.label_search = QLabel("Cauta scorul unui jucator:")
        self.btn_search = QPushButton("Interogare Scor")
        self.btn_search.clicked.connect(self.handleInterogare)

        self.label_search_result = QLabel("")

        layout.addWidget(self.label_search)
        layout.addWidget(self.input_search_user)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.label_search_result)

        self.btn_search_opponent = QPushButton("Cauta Oponent")
        self.btn_search_opponent.clicked.connect(self.cautaOponent)
        layout.addWidget(self.btn_search_opponent)

        self.setLayout(layout)

    def handleInterogare(self):
        user = self.input_search_user.text()
        if not user:
            self.showMessage("Eroare","Introdu un nume de utilizator!", isError=True)
            return
        if not self.dbManager.userExists(user):
            self.showMessage("Eroare", "Utilizator inexistent!")
            return
        else:
            scor = self.dbManager.getPlayerScore(user)
            self.label_search_result.setText(f"Jucatorul '{user}' are {scor} puncte.")

    def cautaOponent(self):
        self.btn_search_opponent.setEnabled(False)
        self.btn_search_opponent.setText("Se cauta oponent...")

        ipc = ipcManager()
        if ipc.connectCreate():
            self.showMessage("Gata de partida","Conectare realizata cu succes. Incepem meciul")

            self.chess_window = ChessWindow(self.dbManager, self.username, ipc)
            self.hide()
            self.chess_window.show()
        else:
            self.showMessage("Eroare", "Nu s-a putut realiza conexiunea de retea", isError=True)
            self.btn_search_opponent.setEnabled(True)
            self.btn_search_opponent.setText("Se cauta oponent...")

class ChessWindow(BaseWindow):
    def __init__(self, dbManager, player, ipc_manager = None):
        self.dbManager = dbManager
        self.player = player
        self.ipc_manager = ipc_manager

        self.logic_board = Board()
        self.piece_symbols = {
            "wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK": "♔", "wP": "♙",
            "bR": "♖", "bN": "♘", "bB": "♗", "bQ": "♕", "bK": "♔", "bP": "♙",
            "": ""
        }

        super().__init__(title=f"Sah Player2Player - Jucator: {self.player}", width=800, height=800)
        self.setFixedSize(800, 800)
        self.buttons = [[None for _ in range(8)] for _ in range(8)]

        self.setupUi()

    def setupUi(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        self.drawBoardUI()
        self.updateBoardUI()

        self.setLayout(self.grid_layout)

    def drawBoardUI(self):
        base_style = "border: none; font-size: 80px; font-family: 'DejaVu Sans'; outline: none;"
        for row in range(8):
            for col in range(8):
                btn = QPushButton()
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.setMinimumSize(1, 1)

                if (row + col) % 2 == 0:
                    btn.setStyleSheet(f"background-color: #2D3E50; {base_style}")
                else:
                    btn.setStyleSheet(f"background-color: #D5D8DC; {base_style}")

                btn.clicked.connect(lambda checked, r=row, c=col: self.onSquareClicked(r, c))

                self.grid_layout.addWidget(btn, row, col)
                self.buttons[row][col] = btn

    def updateBoardUI(self):
        for row in range(8):
            for col in range(8):
                piesa = self.logic_board.getPiece(row, col)
                simbol = self.piece_symbols.get(piesa, "")
                btn = self.buttons[row][col]

                btn.setText(simbol)

                if piesa.startswith("w"):
                    btn.setStyleSheet(btn.styleSheet() + " color: #FFFFFF;")
                elif piesa.startswith("b"):
                    btn.setStyleSheet(btn.styleSheet() + " color: #000000;")

    def onSquareClicked(self, row, col):
        print(f"Ai dat click pe campul: rand {row}, coloana {col}")


if __name__ == "__main__":
    # O scurtă zonă de testare direct în acest fișier
    app = QApplication(sys.argv)


    # Simulam o instantiere cu o baza de date goala
    # In main.py vei folosi DatabaseManager() si flow-ul complet
    class MockDB:
        def loginUser(self, user, passwd): return True

        def registerUser(self, user, passwd): return True

        def userExists(self, user): return True

        def getPlayerScore(self, user): return 0


    mock_db = MockDB()
    login_win = LoginWindow(mock_db)
    register_win = RegisterWindow(mock_db)
    login_win.register_window = register_win
    register_win.loginWindow = login_win

    login_win.show()
    sys.exit(app.exec_())
