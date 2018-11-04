import sys
from PyQt5 import QtWidgets
import MainWindow as MainWindow

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()

    sys.exit(app.exec_())
    