from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import MessageDialog as MessageDialog

class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.setSceneRect(0, 0, 600, 600)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        point = [x, y]
        if point in MainWindow.listPoint:
            self.dialog = MessageDialog.MessageDialog('Point exsit')
            self.dialog.exec_()
        else:
            pen = QtGui.QPen(QtCore.Qt.black)
            brush = QtGui.QBrush(QtCore.Qt.black)
            self.addEllipse(x, y, 1, 1, pen, brush)
        
            MainWindow.listPoint.append(point)
            # Testing
            print(x, y)

class MainWindow(QtWidgets.QMainWindow):
    listPoint = []
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('MainWindow.ui', self)

        self.Btn_Set.clicked.connect(self.listenerSetPoint)
        self.Btn_Run.clicked.connect(self.listenerRun)
        self.Btn_Load.clicked.connect(self.listenerLoadData)

        self.scene = GraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()
    
    def listenerSetPoint(self):
        if self.lineEdit_X.text() != '' and self.lineEdit_Y.text() != '':
            point = [int(self.lineEdit_X.text()), int(self.lineEdit_Y.text())]
            
            if point in self.listPoint:
                self.dialog = MessageDialog.MessageDialog('Point exsit')
                self.dialog.exec_()
            else:
                pen = QtGui.QPen(QtCore.Qt.black)
                brush = QtGui.QBrush(QtCore.Qt.black)
                self.scene.addEllipse(point[0], point[1], 1, 1, pen, brush)
                self.listPoint.append(point)
                    
                self.graphicsView.show()

            self.lineEdit_X.clear()
            self.lineEdit_Y.clear()
        else:
            self.dialog = MessageDialog.MessageDialog('Empty X or Y')
            self.dialog.exec_()

    def listenerRun(self):
        self.scene.clear()

    def listenerLoadData(self):
        self.scene.clear()