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
            MainWindow.listPointCount[0] += 1
            # Testing
            print(x, y)
            print(MainWindow.listPointCount)

    def mouseMoveEvent(self, event):
        self.moved.emit(event)

class MainWindow(QtWidgets.QMainWindow):
    listPoint = []
    listPointCount = [0]
    listConvexLine = []
    listPerpendicularBisector = []
    
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('MainWindow.ui', self)

        self.buttonSet.clicked.connect(self.listenerSet)
        # self.buttonStep.clicked.connect(self.listenerStep)
        self.buttonInput.clicked.connect(self.listenerInput)
        self.buttonRun.clicked.connect(self.listenerRun)
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
                self.listPointCount[0] += 1
                    
                self.graphicsView.show()

            self.lineEdit_X.clear()
            self.lineEdit_Y.clear()
        else:
            self.dialog = MessageDialog.MessageDialog('Empty X or Y')
            self.dialog.exec_()

    def listenerClear(self):
        self.listPoint.clear()
        self.listPointCount.clear()
        self.scene.clear()

        self.listPointCount.append(0)
    
    def listenerInput(self):
        self.listPointCount.clear()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            # Testing
            print(fileName)
            f = open(fileName, 'r')

            while 1:
                line = f.readline()
                line = line[:-1]
                if line.isdigit():
                    size = int(line)
                    if size > 0:
                        self.listPointCount.append(size)
                        for i in range (0, size):
                            point = f.readline().split()
                            point = list(map(int, point))
                            self.listPoint.append(point)
                    else:
                        break

    def listenerRun(self):
        self.listConvexLine.append(QtCore.QLineF(self.listPoint[0][0], self.listPoint[0][1], self.listPoint[1][0], self.listPoint[1][1]))
        self.listConvexLine.append(QtCore.QLineF(self.listPoint[1][0], self.listPoint[1][1], self.listPoint[2][0], self.listPoint[2][1]))
        self.listConvexLine.append(QtCore.QLineF(self.listPoint[2][0], self.listPoint[2][1], self.listPoint[0][0], self.listPoint[0][1]))

        # convex hull
        for i in range(0, 3):
            self.drawConvex(self.listConvexLine[i])

        # Perpendicular Bisector
        self.drawPerpendicularBisector(self.listPoint[0][0], self.listPoint[0][1], self.listPoint[1][0], self.listPoint[1][1])
        self.drawPerpendicularBisector(self.listPoint[1][0], self.listPoint[1][1], self.listPoint[2][0], self.listPoint[2][1])
        self.drawPerpendicularBisector(self.listPoint[2][0], self.listPoint[2][1], self.listPoint[0][0], self.listPoint[0][1])

        # Erase
        temp = QtCore.QPointF(0,0)
        # print(self.listPerpendicularBisector[0].intersect(self.listPerpendicularBisector[0], temp))
        self.listPerpendicularBisector[0].intersect(self.listPerpendicularBisector[1], temp)
        print(temp)     # Find the point

    def drawConvex(self, line):
        self.pen = QtGui.QPen(QtCore.Qt.green)
        # 3 point
        self.scene.addLine(line, self.pen)

    def drawPerpendicularBisector(self, x1, y1, x2, y2):
        midpointX = (x1+x2)/2
        midpointY = (y1+y2)/2
        # Perpendicular Bisector slope
        if (x2-x1) != 0:
            m = -(x2-x1)/(y2-y1)
        else:
            m = 0
        c = midpointY-(m*midpointX)
        
        y1New = m*0+c
        y2New = m*600+c
    
        self.pen = QtGui.QPen(QtCore.Qt.blue)
        line = QtCore.QLineF(0, y1New, 600, y2New)
        self.scene.addLine(line, self.pen)

        self.listPerpendicularBisector.append(line)