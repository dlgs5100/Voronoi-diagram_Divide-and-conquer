from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import MessageDialog as MessageDialog
import operator


class GraphicsScene(QtWidgets.QGraphicsScene):
    moved = QtCore.pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent)
    def __init__(self, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.setSceneRect(0, 0, 600, 600)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()

        # point = QtCore.QPointF(x, y)
        point = [x,y]
        if point in MainWindow.listPoint:
            self.dialog = MessageDialog.MessageDialog('Point exsit')
            self.dialog.exec_()
        else:
            pen = QtGui.QPen(QtCore.Qt.red)
            brush = QtGui.QBrush(QtCore.Qt.red)
            self.addEllipse(x, y, 1, 1, pen, brush)
        
            MainWindow.listPoint.append(point)
            MainWindow.listPointCount[0] += 1
            # Testing mouse set point
            print(x, y)

    def mouseMoveEvent(self, event):
        self.moved.emit(event)

class MainWindow(QtWidgets.QMainWindow):
    listPoint = []
    listPointCount = [0]
    listConvexLine = [] # 擦掉多的，清空
    listPerpendicularBisector = []  # 畫完找完交點，清空
    
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('MainWindow.ui', self)

        self.buttonSet.clicked.connect(self.listenerSet)
        # self.buttonStep.clicked.connect(self.listenerStep)
        self.buttonInput.clicked.connect(self.listenerInput)
        self.buttonRun.clicked.connect(self.listenerRun)
        self.buttonOutput.clicked.connect(self.listenerOutput)
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
            # point = QtCore.QPointF(int(self.lineEdit_X.text()), int(self.lineEdit_Y.text()))
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
        self.listConvexLine.clear()
        self.listPerpendicularBisector.clear()
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
                            data = f.readline().split()
                            point = QtCore.QPointF(list(map(int, data))[0], list(map(int, data))[1])
                            self.listPoint.append(point)
                    else:
                        break

    def listenerOutput(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            # Testing
            print(fileName)
            f = open(fileName, 'w')

    def listenerRun(self):

        self.sortPoint()
        # convex hull
        self.drawConvex(self.listPoint)

        # Perpendicular Bisector 3 point
        for i in range(0, 3):
            self.drawPerpendicularBisector(self.listConvexLine[i])
        
        self.point = self.findIntersectionPoint()

        for i in range(0, 3):
            position = self.determineIntersectionRelativePosition(self.listConvexLine[i] ,self.point)  # 用點去跑
            self.listConvexLine[i] = [self.listConvexLine[i], position]
            self.deleteExceedLine(self.listConvexLine[i], self.point)

    def sortPoint(self):
        list1 = sorted(self.listPoint, key=operator.itemgetter(0, 1))
        for i in range(0, len(self.listPoint)):
            self.listPoint[i] = QtCore.QPointF(list1[i][0], list1[i][1])

    def drawConvex(self, listPoint):
        order = (listPoint[1].x()-listPoint[0].x())*(listPoint[2].y()-listPoint[0].y()) - (listPoint[1].y()-listPoint[0].y())*(listPoint[2].x()-listPoint[0].x())
        if order < 0:   # 逆時針
            print('逆')
            self.listConvexLine.append(QtCore.QLineF(listPoint[0].x(), listPoint[0].y(), listPoint[1].x(), listPoint[1].y()))
            self.listConvexLine.append(QtCore.QLineF(listPoint[1].x(), listPoint[1].y(), listPoint[2].x(), listPoint[2].y()))
            self.listConvexLine.append(QtCore.QLineF(listPoint[2].x(), listPoint[2].y(), listPoint[0].x(), listPoint[0].y()))
        elif order > 0:     # 順時針
            print('順')
            self.listConvexLine.append(QtCore.QLineF(listPoint[0].x(), listPoint[0].y(), listPoint[2].x(), listPoint[2].y()))
            self.listConvexLine.append(QtCore.QLineF(listPoint[2].x(), listPoint[2].y(), listPoint[1].x(), listPoint[1].y()))
            self.listConvexLine.append(QtCore.QLineF(listPoint[1].x(), listPoint[1].y(), listPoint[0].x(), listPoint[0].y()))

        self.pen = QtGui.QPen(QtCore.Qt.green)
        # 3 point
        for i in range(0, 3):
            self.scene.addLine(self.listConvexLine[i], self.pen)

    def drawPerpendicularBisector(self, listConvexLine):
        midpointX = (listConvexLine.x1()+listConvexLine.x2())/2
        midpointY = (listConvexLine.y1()+listConvexLine.y2())/2
        # Perpendicular Bisector slope
        if (listConvexLine.y2()-listConvexLine.y1()) != 0:    # 中垂腺斜率無限
            m = -(listConvexLine.x2()-listConvexLine.x1()) / (listConvexLine.y2()-listConvexLine.y1())
            c = midpointY-(m*midpointX)
            x1New = 0
            if m*x1New+c >= 0 and m*x1New+c <= 600:
                y1New = m*x1New+c
            else:
                y1New = 0
                x1New = (y1New-c)/m

            x2New = 600
            if m*x2New+c >= 0 and m*x2New+c <= 600:
                y2New = m*x2New+c
            else:
                y2New = 600
                x2New = (y2New-c)/m
        else:
            x1New = midpointX
            x2New = midpointX
            y1New = 0
            y2New = 600
    
        self.pen = QtGui.QPen(QtCore.Qt.blue)
        line = QtCore.QLineF(x1New, y1New, x2New, y2New)
        self.scene.addLine(line, self.pen)

        self.listPerpendicularBisector.append(line)

    def findIntersectionPoint(self):
        IntersectionPoint = QtCore.QPointF(0,0)
        result = self.listPerpendicularBisector[0].intersect(self.listPerpendicularBisector[1], IntersectionPoint)
        
        if result == 0:
            print("No Intersection!")
            return None
        else:
            # Testing Intersection point
            print('交點:', round(IntersectionPoint.x(),1), round(IntersectionPoint.y(),1))
            
            # return QtCore.QPointF(round(IntersectionPoint.x(),1), round(IntersectionPoint.y(),1))
            return IntersectionPoint

    def determineIntersectionRelativePosition(self, line, point):
        result = (line.x2()-line.x1())*(point.y()-line.y1()) - (line.y2()-line.y1())*(point.x()-line.x1())
        print(line.x1(), line.y1(), line.x2(), line.y2())
        if result > 0:
            print('right')
            return 'right'
        elif result < 0:
            print('left')
            return 'left'
        else:
            print('line')
            return 'line'

    def deleteExceedLine(self, line, point):
        midPointX = (line[0].x1()+line[0].x2())/2
        midPointY = (line[0].y1()+line[0].y2())/2
        # 交點function回傳精度過高，以此避免
        if abs(midPointX-point.x()) < 0.01:
            midPointX = point.x() 
        if abs(midPointY-point.y()) < 0.01:
            midPointY = point.y() 
        
        # 由逆時針順序判斷點在線的哪邊
        if line[1] == 'left':
            vectorX = point.x()-midPointX
            vectorY = point.y()-midPointY
        elif line[1] == 'right':
            vectorX = midPointX-point.x()
            vectorY = midPointY-point.y()
        else:
            vectorX = 0
            vectorY = 0

        
        if (point.x()-midPointX) != 0:  # 正常情況
            m = (point.y()-midPointY) / (point.x()-midPointX)
            c = point.y()-(m*point.x())
        else:
            if (point.y()-midPointY) == 0: # 交點在線上
                m = -(line[0].x1()-line[0].x2()) / (line[0].y1()-line[0].y2())
                c = point.y()-(m*point.x())

        
        if vectorX > 0:
            drawPointX = 600
            if vectorY != 0:
                drawPointY = m*drawPointX+c
            else:
                drawPointY = point.y()
        elif vectorX < 0:
            drawPointX = 0
            if vectorY != 0:
                drawPointY = m*drawPointX+c
            else:
                drawPointY = point.y()
        else:
            drawPointX = point.x()
            if vectorY > 0: # 垂直
                drawPointY = 600
            elif vectorY < 0: # 水平
                drawPointY = 0
            else: # 點在線上
                if line[0].x1()-line[0].x2() > 0 and line[0].y1()-line[0].y2() > 0:
                    drawPointX = 0
                elif line[0].x1()-line[0].x2() > 0 and line[0].y1()-line[0].y2() < 0: 
                    drawPointX = 600
                elif line[0].x1()-line[0].x2() < 0 and line[0].y1()-line[0].y2() > 0: 
                    drawPointX = 0
                elif line[0].x1()-line[0].x2() < 0 and line[0].y1()-line[0].y2() < 0: 
                    drawPointX = 600
                drawPointY = m*drawPointX+c

        if drawPointX != point.x() or drawPointY != point.y():
            self.pen = QtGui.QPen(QtCore.Qt.white)
            eraseLine = QtCore.QLineF(point.x(), point.y(), drawPointX, drawPointY)
            self.scene.addLine(eraseLine, self.pen)
    