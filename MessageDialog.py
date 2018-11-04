from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

class MessageDialog(QtWidgets.QDialog):
    def __init__(self, message):
        super(MessageDialog,self).__init__()
        loadUi('MessageDialog.ui', self)

        self.labelMessage.setText(message)
        self.buttonOK.clicked.connect(self.listenerClose)
    
    def listenerClose(self):
        self.close()