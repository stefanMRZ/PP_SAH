import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget

class BaseWindow(QWidget):
    def __init__(self, title = "Sah Player2Player", width = 400, height = 300):
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


