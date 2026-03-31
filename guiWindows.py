import sys

from PyQt5.QtCore import QTimer
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
        self.input_password.returnPressed.connect(self.handleLogin)

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
        self.adversar = None
        self.ipc = None
        self.match_timer = QTimer()
        self.match_timer.timeout.connect(self.asteaptaNegru)
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

        self.ipc = ipcManager()
        if self.ipc.connectCreate():
            mesaj = self.ipc.receiveMessage(msg_type=1)
            if mesaj and mesaj.startswith("Hello:"):
                self.adversar = mesaj.split(":")[1]
                self.ipc.sendMessage(f"Hai noroc:{self.username}", msg_type=2)
                self.showMessage("Meci gasit!", "Te-ai conectat. Vei juca cu NEGRU.")
                self.pornesteJocul("b", self.adversar)
            else:
                self.ipc.sendMessage(f"Hello:{self.username}", msg_type=1)
                self.match_timer.start(500)
        else:
            self.showMessage("Eroare", "Nu s-a putut realiza conexiunea de retea", isError=True)
            self.btn_search_opponent.setEnabled(True)
            self.btn_search_opponent.setText("Se cauta oponent...")

    def asteaptaNegru(self):
        raspuns = self.ipc.receiveMessage(msg_type=2)
        if raspuns and raspuns.startswith("Hai noroc:"):
            self.adversar = raspuns.split(":")[1]
            self.match_timer.stop()
            self.showMessage("Meci gasit!", "Un adversar s-a conectat! Vei juca cu ALB.")
            self.pornesteJocul("w",self.adversar)

    def pornesteJocul(self, culoare, adversar):
        self.chess_window = ChessWindow(self.dbManager, self.username, self.ipc, culoare, adversar)
        self.hide()
        self.chess_window.show()

class ChessWindow(BaseWindow):
    def __init__(self, dbManager, player, ipc_manager, assigned_color, adversar):
        self.selected_square = None
        self.adversar = adversar
        self.dbManager = dbManager
        self.player = player
        self.ipc_manager = ipc_manager
        self.assigned_color = assigned_color
        self.turn = "w"

        self.logic_board = Board()
        self.piece_symbols = {
            "wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK": "♔", "wP": "♙",
            "bR": "♖", "bN": "♘", "bB": "♗", "bQ": "♕", "bK": "♔", "bP": "♙",
            "": ""
        }

        scor_p1, scor_p2 = self.dbManager.getRivalScore(player, adversar)
        titlu = f"{player}:        {scor_p1} - {scor_p2}        :{adversar}"
        super().__init__(title=titlu, width=800, height=800)
        self.setFixedSize(800, 800)
        self.buttons = [[None for _ in range(8)] for _ in range(8)]


        self.setupUi()
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkOppnentMove)
        self.timer.start(500)

    def setupUi(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        self.drawBoardUI()
        self.updateBoardUI()

        self.setLayout(self.grid_layout)

    def checkOppnentMove(self):
        if not self.ipc_manager:
            return
        tip = 2 if self.assigned_color == "w" else 1
        mesaj = self.ipc_manager.receiveMessage(msg_type=tip)
        if mesaj:
            try:
                coords = list(map(int, mesaj.split(",")))
                old_r, old_c, new_r, new_c = coords

                piesa = self.logic_board.board[old_r][old_c]
                self.logic_board.board[new_r][new_c] = piesa
                self.logic_board.board[old_r][old_c] = ""

                self.turn = "b" if self.turn == "w" else "w"
                self.updateBoardUI()
                print(f"Adversarul a mutat de la {old_r},{old_c} la {new_r},{new_c}")
            except Exception as e:
                print(f"Eroare la procesare mesaj IPC: {e}")

    def drawBoardUI(self):
        base_style = "border: none; font-size: 80px; font-family: 'DejaVu Sans'; outline: none;"
        for row in range(8):
            for col in range(8):
                btn = QPushButton()
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.setMinimumSize(1, 1)

                if (row + col) % 2 == 0:
                    btn.setStyleSheet(f"background-color: #D5D8DC; {base_style}")
                else:
                    btn.setStyleSheet(f"background-color: #2D3E50; {base_style}")

                btn.clicked.connect(lambda checked, r=row, c=col: self.onSquareClicked(r, c))

                if self.assigned_color == "w":
                    viz_row = row
                    viz_col = col
                else:
                    viz_row = 7 - row
                    viz_col = 7 - col

                self.grid_layout.addWidget(btn, viz_row, viz_col)
                self.buttons[row][col] = btn

    def updateBoardUI(self):
        for row in range(8):
            for col in range(8):
                piesa = self.logic_board.getPiece(row, col)
                simbol = self.piece_symbols.get(piesa, "")
                btn = self.buttons[row][col]

                btn.setText(simbol)

                if (row + col) % 2 == 0:
                    color = "#D5D8DC"
                else:
                    color = "#2D3E50"

                base_style = f"background-color: {color}; border: none; font-size: 80px; font-family: 'DejaVu Sans';"
                if piesa.startswith("w"):
                    btn.setStyleSheet(base_style + " color: white;")
                elif piesa.startswith("b"):
                    btn.setStyleSheet(base_style + " color: black;")
                else:
                    btn.setStyleSheet(base_style)

    def onSquareClicked(self, row, col):
        if self.turn != self.assigned_color:
            print("Asteapta adversarul!")
            return

        piece = self.logic_board.getPiece(row, col)

        if self.selected_square is None:
            if piece != "" and piece.startswith(self.assigned_color):
                self.selected_square = (row, col)
                self.buttons[row][col].setStyleSheet(self.buttons[row][col].styleSheet() + "border: 3px solid yellow;")
            return

        else:
            old_row, old_col = self.selected_square
            self.selected_square = None

            if old_row == row and old_col == col:
                self.updateBoardUI()
                return

            if self.logic_board.board[row][col].startswith(self.assigned_color):
                self.selected_square = (row, col)
                self.updateBoardUI()
                self.buttons[row][col].setStyleSheet(self.buttons[row][col].styleSheet() + "border: 4px solid yellow;")
                return

            piesa_de_mutat = self.logic_board.board[old_row][old_col]
            print(f"DEBUG: Mut piesa '{piesa_de_mutat}' de la {old_row},{old_col} la {row},{col}")

            self.logic_board.board[row][col] = piesa_de_mutat
            self.logic_board.board[old_row][old_col] = ""

            if self.ipc_manager:
                tip = 1 if self.assigned_color == "w" else 2
                mesaj_mutare = f"{old_row},{old_col},{row},{col}"
                self.ipc_manager.sendMessage(mesaj_mutare, tip)

            self.turn = "b" if self.turn == "w" else "w"

            self.updateBoardUI()
            print(f"Mutat la {row},{col}. Acum e randul: {self.turn}")

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
