from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import MessageDialog as MessageDialog

class GraphicsScene(QtWidgets.QGraphicsScene):
    moved = QtCore.pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent)
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
            pen = QtGui.QPen(QtCore.Qt.red)
            brush = QtGui.QBrush(QtCore.Qt.red)
            self.addEllipse(x, y, 1, 1, pen, brush)
        
            MainWindow.listPoint.append(point)
            # Testing
            print(x, y)

    def mouseMoveEvent(self, event):
        self.moved.emit(event)

class MainWindow(QtWidgets.QMainWindow):
    listPoint = []
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('MainWindow.ui', self)

        self.buttonSet.clicked.connect(self.listenerSet)
        # self.buttonStep.clicked.connect(self.listenerStep)
        self.buttonInput.clicked.connect(self.listenerInput)
        # self.buttonRun.clicked.connect(self.listenerRun)
        # self.buttonOutput.clicked.connect(self.listenerOutput)
        self.buttonClear.clicked.connect(self.listenerClear)

        self.scene = GraphicsScene(self)
        self.scene.moved.connect(self.listenerAutoXY)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()
    def listenerAutoXY(self, arg):
        self.labelAutoX.setText(str(arg.scenePos().x()))
        self.labelAutoY.setText(str(arg.scenePos().y()))

    def listenerSet(self):
        if self.lineEdit_X.text() != '' and self.lineEdit_Y.text() != '':
            point = [int(self.lineEdit_X.text()), int(self.lineEdit_Y.text())]
            
            if point in self.listPoint:
                self.dialog = MessageDialog.MessageDialog('Point exsit')
                self.dialog.exec_()
            else:
                pen = QtGui.QPen(QtCore.Qt.red)
                brush = QtGui.QBrush(QtCore.Qt.red)
                self.scene.addEllipse(point[0], point[1], 1, 1, pen, brush)
                self.listPoint.append(point)
                    
                self.graphicsView.show()

            self.lineEdit_X.clear()
            self.lineEdit_Y.clear()
        else:
            self.dialog = MessageDialog.MessageDialog('Empty X or Y')
            self.dialog.exec_()

    def listenerClear(self):
        self.listPoint.clear()
        self.scene.clear()
    
    def listenerInput(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            # Testing
            print(fileName)
            f = open(fileName, 'r')

            while 1:
                size = int(f.readline())
                if size > 0:
                    for i in range (0, size):
                        point = f.readline().split()
                        point = list(map(int, point))
                        self.listPoint.append(point)
                else:
                    print(size)
                    break

    def draw(self):
        print(123)