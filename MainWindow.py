from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import MessageDialog as MessageDialog
import operator
import numpy
import math
import random
import copy

mode = 'None'  # 作為判斷為讀檔或手動


class GraphicsScene(QtWidgets.QGraphicsScene):
    moved = QtCore.pyqtSignal(QtWidgets.QGraphicsSceneMouseEvent)

    def __init__(self, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.setSceneRect(0, 0, 600, 600)

    def mousePressEvent(self, event):
        global mode
        x = event.scenePos().x()
        y = event.scenePos().y()

        # point = QtCore.QPointF(x, y)
        point = [x, y]
        if mode == 'None' or mode == 'user':
            if point in MainWindow.loadPoint:
                self.dialog = MessageDialog.MessageDialog('Point exsit')
                self.dialog.exec_()
            else:
                pen = QtGui.QPen(QtCore.Qt.red)
                brush = QtGui.QBrush(QtCore.Qt.red)
                self.addEllipse(x, y, 1, 1, pen, brush)

                MainWindow.loadPoint.append(point)
                if not MainWindow.listPointCount:
                    MainWindow.listPointCount.append(0)
                MainWindow.listPointCount[0] += 1
                # Testing mouse set point
                print(x, y)
                mode = 'user'
        else:
            self.dialog = MessageDialog.MessageDialog("Can't enter now!")
            self.dialog.exec_()

    def mouseMoveEvent(self, event):
        self.moved.emit(event)


class MainWindow(QtWidgets.QMainWindow):
    loadPoint = []  # 讀檔為雙層list，手動僅單層list
    listPointCount = []  # 判斷多組測資有幾個點，手動必只有一組
    listConvexLine = []  # 擦掉多的，清空
    resultPoint = []
    resultLine = []

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('MainWindow.ui', self)

        self.buttonSet.clicked.connect(self.listenerSet)
        self.buttonStep.clicked.connect(self.listenerStep)
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
        global mode
        if self.lineEdit_X.text() != '' and self.lineEdit_Y.text() != '':
            if (int(self.lineEdit_X.text()) >= 0 and int(self.lineEdit_X.text()) <= 600) and (int(self.lineEdit_Y.text()) >= 0 and int(self.lineEdit_Y.text()) <= 600):
                if mode == 'None' or mode == 'user':
                    # point = QtCore.QPointF(int(self.lineEdit_X.text()), int(self.lineEdit_Y.text()))
                    point = [int(self.lineEdit_X.text()),
                                 int(self.lineEdit_Y.text())]

                    if point in self.loadPoint:
                        self.dialog = MessageDialog.MessageDialog(
                            'Point exsit')
                        self.dialog.exec_()
                    else:
                        pen = QtGui.QPen(QtCore.Qt.red)
                        brush = QtGui.QBrush(QtCore.Qt.red)
                        self.scene.addEllipse(
                            point[0], point[1], 1, 1, pen, brush)
                        self.loadPoint.append(point)
                        if not self.listPointCount:
                            self.listPointCount.append(0)
                        self.listPointCount[0] += 1

                        self.graphicsView.show()

                    self.lineEdit_X.clear()
                    self.lineEdit_Y.clear()

                    mode = 'user'
                else:
                    self.dialog = MessageDialog.MessageDialog(
                        "Can't enter now!")
                    self.dialog.exec_()
            else:
                self.dialog = MessageDialog.MessageDialog(
                    'X or Y out of range')
                self.dialog.exec_()
        else:
            self.dialog = MessageDialog.MessageDialog('X or Y empty')
            self.dialog.exec_()

    def listenerClear(self):
        global mode
        mode = 'None'
        self.loadPoint.clear()
        self.listPointCount.clear()
        self.listConvexLine.clear()
        self.resultPoint.clear()
        self.resultLine.clear()
        self.scene.clear()

    def listenerInput(self):
        global mode
        if mode == 'None':
            self.listPointCount.clear()
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
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
                            for i in range(0, size):
                                data = f.readline().split()
                                # point = QtCore.QPointF(list(map(int, data))[0], list(map(int, data))[1])
                                point = [list(map(int, data))[0],
                                              list(map(int, data))[1]]
                                self.loadPoint.append(point)
                        else:
                            break
                self.labelAutoAmount.setText(str(len(self.listPointCount)))
                print(self.loadPoint)

                mode = 'file'
        else:
            self.dialog = MessageDialog.MessageDialog("Can't load file now!")
            self.dialog.exec_()

    def listenerOutput(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            # Testing
            print(fileName)
            f = open(fileName, 'w')
            for i in range(0, len(self.resultPoint)):
                f.write('P ')
                f.write(str(int(self.resultPoint[i][0])))
                f.write(' ')
                f.write(str(int(self.resultPoint[i][1])))
                f.write('\n')

            for i in range(0, len(self.resultLine)):
                f.write('E ')
                f.write(str(int(self.resultLine[i][0])))
                f.write(' ')
                f.write(str(int(self.resultLine[i][1])))
                f.write(' ')
                f.write(str(int(self.resultLine[i][2])))
                f.write(' ')
                f.write(str(int(self.resultLine[i][3])))
                f.write('\n')

    def listenerRun(self):
        global mode
        self.resultPoint.clear()
        self.resultLine.clear()
        self.listConvexLine.clear()

        listPoint = []
        if len(self.listPointCount) == 0:
            mode = 'None'
            self.dialog = MessageDialog.MessageDialog('Out of data!')
            self.dialog.exec_()
        else:
            for i in range(0, self.listPointCount[0]):
                listPoint.append(self.loadPoint[0])
                self.loadPoint.pop(0)
            self.listPointCount.pop(0)

            # 為了讓讀檔點有顏色
            if mode != 'user':
                self.scene.clear()
                pen = QtGui.QPen(QtCore.Qt.red)
                brush = QtGui.QBrush(QtCore.Qt.red)
                for i in range(0, len(listPoint)):
                    self.scene.addEllipse(
                        listPoint[i][0], listPoint[i][1], 1, 1, pen, brush)

            self.labelAutoAmount.setText(str(len(self.listPointCount)))
            self.resultPoint, listPoint = self.sortPoint(
                listPoint)  # resultPoint型態為list，listPoint型態為PointF
            # print(listPoint)

            if self.hasDuplicate(listPoint) == False:
                self.dividePoint(listPoint)

                # # convex hull
                # self.drawConvex(listPoint)

                # self.drawPerpendicularBisector(self.listConvexLine)

                # self.point = self.findIntersectionPoint(self.listConvexLine)

                # #判斷有無交點
                # if self.point != None:
                #     for i in range(0, len(self.listConvexLine)):
                #         position = self.determineIntersectionRelativePosition(self.listConvexLine[i][0] ,self.point)
                #         self.listConvexLine[i].append(position)
                #         self.deleteExceedLine(self.listConvexLine[i], self.point)

                #     pen = QtGui.QPen(QtCore.Qt.blue)
                #     brush = QtGui.QBrush(QtCore.Qt.blue)
                #     self.scene.addEllipse(self.point.x(), self.point.y(), 1, 1, pen, brush)

                # self.resultLine = self.sortLine()
            else:
                self.dialog = MessageDialog.MessageDialog(
                    "Exist duplicate data!")
                self.dialog.exec_()

    def listenerStep(self):
        print(123)

    def sortPoint(self, listPoint):
        resultList = sorted(listPoint, key=operator.itemgetter(0, 1))
        for i in range(0, len(listPoint)):
            listPoint[i] = QtCore.QPointF(resultList[i][0], resultList[i][1])

        return resultList, listPoint

    def sortLine(self):
        resultList = []
        for i in range(0, len(self.listConvexLine)):
            line = [round(self.listConvexLine[i][1].x1(), 0), round(self.listConvexLine[i][1].y1(), 0), round(self.listConvexLine[i][1].x2(), 0), round(self.listConvexLine[i][1].y2(), 0)]
            resultList.append(line)
        resultList = sorted(resultList, key=operator.itemgetter(0, 1, 2, 3))

        return resultList

    def dividePoint(self, listPoint):
        amount = len(listPoint)
        listLocalConvexLine = []
        if amount > 3:
            listLocalConvexLine1 = self.dividePoint(listPoint[:math.ceil(amount/2)])    # 左部
            listLocalConvexLine2 = self.dividePoint(listPoint[math.ceil(amount/2):])    # 右部

            # self.scene.clear()
            listMergeConvexLine, listLeftInnerConvexLine, listLeftPerpendicularBisector, listRightInnerConvexLine, listRightPerpendicularBisector = self.mergeConvex(listLocalConvexLine1, listLocalConvexLine2)

            pen = QtGui.QPen(QtCore.Qt.black)
            # pen = QtGui.QPen(QtGui.QColor(random.randint(30,255), random.randint(30,255), random.randint(30,255)))
            for item in listMergeConvexLine:
                self.scene.addLine(item, pen)
            pen1 = QtGui.QPen(QtCore.Qt.black)
            # pen1 = QtGui.QPen(QtGui.QColor(random.randint(30,255), random.randint(30,255), random.randint(30,255)))
            for item in listLeftInnerConvexLine:
                self.scene.addLine(item[0], pen1)
                self.scene.addLine(item[1], pen1)
            for item in listRightInnerConvexLine:
                self.scene.addLine(item[0], pen1)
                self.scene.addLine(item[1], pen1)

            self.getHyperplane(listLeftInnerConvexLine, listLeftPerpendicularBisector, listRightInnerConvexLine, listRightPerpendicularBisector)

        else:
            print(listPoint)
            listLocalConvexLine = self.drawConvex(listPoint)
            listLocalConvexLine = self.drawPerpendicularBisector(listLocalConvexLine)
            if len(listLocalConvexLine) < 2:
                intersectionPoint = None
            else:
                intersectionPoint = self.findIntersectionPoint(listLocalConvexLine[0][1], listLocalConvexLine[1][1])

            # 判斷有無交點
            if intersectionPoint != None:
                for i in range(0, len(listLocalConvexLine)):
                    position = self.determineIntersectionRelativePosition(listLocalConvexLine[i][0], intersectionPoint)
                    listLocalConvexLine[i].append(position)
                    self.deleteExceedLine(listLocalConvexLine[i], intersectionPoint)

                # 補上被擦掉的交點
                pen = QtGui.QPen(QtCore.Qt.blue)
                brush = QtGui.QBrush(QtCore.Qt.blue)
                self.scene.addEllipse(intersectionPoint.x(), intersectionPoint.y(), 1, 1, pen, brush)

            return listLocalConvexLine
            # self.resultLine = self.sortLine()

    def getHyperplane(self, listLeftInnerConvexLine, listLeftPerpendicularBisector, listRightInnerConvexLine, listRightPerpendicularBisector):
        listAuxiliaryLine = []
        listHyperplane = []
        listLeftPoint = []
        listLeftPoint = self.getConvexPoint(listLeftInnerConvexLine)
        listRightPoint = self.getConvexPoint(listRightInnerConvexLine)
        listLeftPoint = sorted(listLeftPoint, key=lambda s: s.y())
        listRightPoint = sorted(listRightPoint, key=lambda s: s.y())
        touchPos = 'Null'

        # 第一條虛線，先左連右試試看
        indexLeft = 0
        indexRight = 0
        indexHyperplane = 0
        latestX2 = 0
        latestY2 = 0
        isFirstHyperplane = True
        for i in range(0,3):
            # if len(listLeftPoint) == indexLeft or len(listRightPoint) == indexRight:
            #     break
            # Hyperplane輔助線
            listAuxiliaryLine.append(QtCore.QLineF(listRightPoint[indexRight], listLeftPoint[indexLeft]))
            pen = QtGui.QPen(QtCore.Qt.blue)
            self.scene.addLine(listAuxiliaryLine[i], pen)

            # 每次都用輔助線重新畫中垂線
            temp = copy.deepcopy(listAuxiliaryLine)
            listHyperplane = copy.deepcopy(self.drawPerpendicularBisector(temp))

            print('latestX2:', latestX2)
            print('latestY2:', latestY2)
            #讓線P1是上面，P2是下面
            if listHyperplane[indexHyperplane][1].y1() > listHyperplane[indexHyperplane][1].y2():
                temp = listHyperplane[indexHyperplane][1].p1()
                listHyperplane[indexHyperplane][1].setP1(listHyperplane[0][1].p2())
                listHyperplane[indexHyperplane][1].setP2(temp)
            elif listHyperplane[indexHyperplane][1].y1() == listHyperplane[indexHyperplane][1].y2():
                print('Error in getHyperplane()')
            
            if isFirstHyperplane == False:
                listHyperplane[indexHyperplane][1].setP1(QtCore.QPointF(latestX2, latestY2))

            intersectionPoint = QtCore.QPointF(600, 600) # Initialize
            for item in listLeftPerpendicularBisector:
                point = self.findIntersectionPoint(listHyperplane[indexHyperplane][1], item)
                if point != None and point.y() < intersectionPoint.y() and point.y() > listHyperplane[indexHyperplane][1].y1():
                    intersectionPoint = point
                    touchPos = 'Left'
            for item in listRightPerpendicularBisector:
                point = self.findIntersectionPoint(listHyperplane[indexHyperplane][1], item)
                if point != None and point.y() < intersectionPoint.y() and point.y() > listHyperplane[indexHyperplane][1].y1():
                    intersectionPoint = point
                    touchPos = 'Right'
            # for item in listLeftInnerConvexLine:
            #     point = self.findIntersectionPoint(listHyperplane[indexHyperplane][1], item[1])
            #     if point != None and point.y() < intersectionPoint.y():
            #         intersectionPoint = point
            #         touchPos = 'Left'
            # for item in listRightInnerConvexLine:
            #     point = self.findIntersectionPoint(listHyperplane[indexHyperplane][1], item[1])
            #     if point != None and point.y() < intersectionPoint.y():
            #         intersectionPoint = point
            #         touchPos = 'Right'

            print(touchPos)
            listHyperplane[indexHyperplane][1].setP2(intersectionPoint)
            latestX2 = intersectionPoint.x()
            latestY2 = intersectionPoint.y()

            pen = QtGui.QPen(QtCore.Qt.red)
            self.scene.addLine(listHyperplane[indexHyperplane][1], pen)

            indexHyperplane += 1
            if touchPos == 'Left':
                indexLeft = indexHyperplane
            elif touchPos == 'Right':
                indexRight = indexHyperplane
            else:
                print('Hyperplane error')

            # latestY2 = listHyperplane[indexHyperplane][1].y2()
            isFirstHyperplane = False

    def drawConvex(self, listPoint):
        listLocalConvexLine = []
        # 將讀入典改為逆時針
        if len(listPoint) == 2:
            listLocalConvexLine.append(QtCore.QLineF(
                listPoint[0].x(), listPoint[0].y(), listPoint[1].x(), listPoint[1].y()))
        elif len(listPoint) == 3:
            # 先畫前三個點
            order = (listPoint[1].x()-listPoint[0].x())*(listPoint[2].y()-listPoint[0].y()) - (
                listPoint[1].y()-listPoint[0].y())*(listPoint[2].x()-listPoint[0].x())
            if order < 0:   # 原逆時針
                # print('逆')
                listLocalConvexLine.append(QtCore.QLineF(
                    listPoint[0].x(), listPoint[0].y(), listPoint[1].x(), listPoint[1].y()))
                listLocalConvexLine.append(QtCore.QLineF(
                    listPoint[1].x(), listPoint[1].y(), listPoint[2].x(), listPoint[2].y()))
                listLocalConvexLine.append(QtCore.QLineF(
                    listPoint[2].x(), listPoint[2].y(), listPoint[0].x(), listPoint[0].y()))
            elif order > 0:     # 原順時針
                # print('順')
                listLocalConvexLine.append(QtCore.QLineF(
                    listPoint[0].x(), listPoint[0].y(), listPoint[2].x(), listPoint[2].y()))
                listLocalConvexLine.append(QtCore.QLineF(
                    listPoint[2].x(), listPoint[2].y(), listPoint[1].x(), listPoint[1].y()))
                listLocalConvexLine.append(QtCore.QLineF(
                    listPoint[1].x(), listPoint[1].y(), listPoint[0].x(), listPoint[0].y()))
            else:
                # print('共')
                listLocalConvexLine.append(QtCore.QLineF(
                    listPoint[0].x(), listPoint[0].y(), listPoint[1].x(), listPoint[1].y()))
                listLocalConvexLine.append(QtCore.QLineF(
                    listPoint[1].x(), listPoint[1].y(), listPoint[2].x(), listPoint[2].y()))

        pen = QtGui.QPen(QtGui.QColor(random.randint(30, 255), random.randint(30,255), random.randint(30,255)))
        # 3 point
        # for i in range(0, len(listLocalConvexLine)):
        #     self.scene.addLine(listLocalConvexLine[i], pen)

        return listLocalConvexLine

    # 1.還未考慮水平and共線
    # 2.兩條線之中其中一點畫在裡面
    def mergeConvex(self, listLocalConvexLine1, listLocalConvexLine2):
        # merge結果
        listMergeConvexLine1 = []
        listMergeConvexLine2 = []
        # listMergePerpendicularBisector = []
        listLeftInnerConvexLine = []
        listRightInnerConvexLine = []
        # 取得所有convex hull上的點
        listPoint1 = self.getConvexPoint(listLocalConvexLine1)
        listPoint2 = self.getConvexPoint(listLocalConvexLine2)
        # 左邊找最下，右邊找最上
        max_Y = 0
        min_Y = 600
        for item in listPoint1:
            if item.y() > max_Y:
                max_Y = item.y()
        for item in listPoint2:
            if item.y() < min_Y:
                min_Y = item.y()

        # 複製
        temp1 = []
        temp2 = []
        for i in range(len(listLocalConvexLine1)):
            temp1.append(listLocalConvexLine1[i][0])
        listMergeConvexLine1 = copy.deepcopy(temp1)
        listLeftInnerConvexLine = copy.deepcopy(listMergeConvexLine1)
        for i in range(len(listLocalConvexLine2)):
            temp2.append(listLocalConvexLine2[i][0])
        listMergeConvexLine2 = copy.deepcopy(temp2)
        listRightInnerConvexLine = copy.deepcopy(listMergeConvexLine2)

        if len(listMergeConvexLine1) == 1:  # 只有兩點構成的一條線
            listMergeConvexLine1.append(QtCore.QLineF(listMergeConvexLine1[0].x2(
            ), listMergeConvexLine1[0].y2(), listMergeConvexLine1[0].x1(), listMergeConvexLine1[0].y1()))
        # 用左邊所有線依序跑右邊所有點
        for i in range(len(listPoint2)):
            for j in range(len(listMergeConvexLine1)):
                if listMergeConvexLine1[j] != None:
                    direction = self.determineIntersectionRelativePosition(
                        listMergeConvexLine1[j], listPoint2[i])
                    if direction == 'right':
                        if listMergeConvexLine1[j].y1() == max_Y:
                            listMergeConvexLine1[j].setP2(listPoint2[i])
                        else:
                            listMergeConvexLine1[j] = None  # 不是最底的直接改成None

        if len(listMergeConvexLine2) == 1:  # 只有兩點構成的一條線
            listMergeConvexLine2.append(QtCore.QLineF(listMergeConvexLine2[0].x2(
            ), listMergeConvexLine2[0].y2(), listMergeConvexLine2[0].x1(), listMergeConvexLine2[0].y1()))
            # 用右邊所有線依序跑左邊所有點
        for i in range(len(listPoint1)):
            for j in range(len(listMergeConvexLine2)):
                if listMergeConvexLine2[j] != None:
                    direction = self.determineIntersectionRelativePosition(
                        listMergeConvexLine2[j], listPoint1[i])
                    if direction == 'right':
                        if listMergeConvexLine2[j].y1() == min_Y:
                            listMergeConvexLine2[j].setP2(listPoint1[i])
                        else:
                            listMergeConvexLine2[j] = None  # 不是最高的直接改成None

        try:
            listMergeConvexLine1.remove(None)
        except ValueError:
            pass

        for item in listMergeConvexLine2:
            if item not in listMergeConvexLine1 and item != None:
                listMergeConvexLine1.append(item)

        # 所有中垂線
        listLeftPerpendicularBisector = []
        listRightPerpendicularBisector = []
        for item in listLocalConvexLine1:
            listLeftPerpendicularBisector.append(item[1])
        for item in listLocalConvexLine2:
            listRightPerpendicularBisector.append(item[1])

        # 取得內部被刪除的convex邊(左)
        if len(listLeftInnerConvexLine) > 2:
            for item in listMergeConvexLine1:
                if item in listLeftInnerConvexLine:
                    listLeftInnerConvexLine.remove(item)
        # 讓inner convex hull的線包含中垂(暫時不用)
        for i in range(len(listLeftInnerConvexLine)):
            for j in range(len(listLocalConvexLine1)):
                if listLeftInnerConvexLine[i] == listLocalConvexLine1[j][0]:
                    listLeftInnerConvexLine[i] = [
                        listLeftInnerConvexLine[i], listLocalConvexLine1[j][1]]

        # 取得內部被刪除的convex邊(右)
        if len(listRightInnerConvexLine) > 2:
            for item in listMergeConvexLine2:
                if item in listRightInnerConvexLine:
                    listRightInnerConvexLine.remove(item)
        # 讓inner convex hull的線包含中垂(暫時不用)
        for i in range(len(listRightInnerConvexLine)):
            for j in range(len(listLocalConvexLine2)):
                if listRightInnerConvexLine[i] == listLocalConvexLine2[j][0]:
                    listRightInnerConvexLine[i] = [
                        listRightInnerConvexLine[i], listLocalConvexLine2[j][1]]

        return listMergeConvexLine1, listLeftInnerConvexLine, listLeftPerpendicularBisector, listRightInnerConvexLine, listRightPerpendicularBisector

    def getConvexPoint(self, listLocalConvexLine):
        listPoint = []
        for i in range(len(listLocalConvexLine)):
            point1 = QtCore.QPointF(
                listLocalConvexLine[i][0].x1(), listLocalConvexLine[i][0].y1())
            point2 = QtCore.QPointF(
                listLocalConvexLine[i][0].x2(), listLocalConvexLine[i][0].y2())
            if point1 not in listPoint:
                listPoint.append(point1)
            if point2 not in listPoint:
                listPoint.append(point2)
        return listPoint

    def drawPerpendicularBisector(self, listLocalConvexLine):

        pen = QtGui.QPen(QtGui.QColor(random.randint(30, 255), random.randint(30,255), random.randint(30,255)))
        for i in range(0, len(listLocalConvexLine)):
            midpointX = (listLocalConvexLine[i].x1(
            )+listLocalConvexLine[i].x2())/2
            midpointY = (listLocalConvexLine[i].y1(
            )+listLocalConvexLine[i].y2())/2
            # Perpendicular Bisector slope
            if (listLocalConvexLine[i].y2()-listLocalConvexLine[i].y1()) != 0:    # 中垂腺斜率無限
                m = -(listLocalConvexLine[i].x2()-listLocalConvexLine[i].x1()) / (
                    listLocalConvexLine[i].y2()-listLocalConvexLine[i].y1())
                c = midpointY-(m*midpointX)
                if m > 0:
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
                elif m < 0:
                    x1New = 0
                    if m*x1New+c >= 0 and m*x1New+c <= 600:
                        y1New = m*x1New+c
                    else:
                        y1New = 600
                        x1New = (y1New-c)/m
                    x2New = 600
                    if m*x2New+c >= 0 and m*x2New+c <= 600:
                        y2New = m*x2New+c
                    else:
                        y2New = 0
                        x2New = (y2New-c)/m
                else:
                    x1New = 0
                    x2New = 600
                    y1New = midpointY
                    y2New = midpointY
            else:
                x1New = midpointX
                x2New = midpointX
                y1New = 0
                y2New = 600

            line = QtCore.QLineF(x1New, y1New, x2New, y2New)
            # self.scene.addLine(line, pen)

            # 將該convex line的中垂線資訊加入list中，
            listLocalConvexLine[i] = [listLocalConvexLine[i], line]

        return listLocalConvexLine

    def findIntersectionPoint(self, line1, line2):
        IntersectionPoint = QtCore.QPointF(0, 0)
        # 用前兩個convex line去找交點
        result = line1.intersect(line2, IntersectionPoint)

        if result == 0:
            print("No Intersection!")
            return None
        else:
            # Testing Intersection point
            print('交點:', round(IntersectionPoint.x(), 1), round(IntersectionPoint.y(),1))

            # return QtCore.QPointF(round(IntersectionPoint.x(),1), round(IntersectionPoint.y(),1))
            return IntersectionPoint

    def determineIntersectionRelativePosition(self, convexLine, point):
        result = (convexLine.x2()-convexLine.x1())*(point.y()-convexLine.y1()) - \
                  (convexLine.y2()-convexLine.y1())*(point.x()-convexLine.x1())
        # print(convexLine.x1(), convexLine.y1(), convexLine.x2(), convexLine.y2())
        if result > 0:
            # print('right')
            return 'right'
        elif result < 0:
            # print('left')
            return 'left'
        else:
            # print('line')
            return 'line'

    def deleteExceedLine(self, convexLine, point):
        midPointX = (convexLine[0].x1()+convexLine[0].x2())/2
        midPointY = (convexLine[0].y1()+convexLine[0].y2())/2
        # 交點function回傳精度過高，以此避免
        if abs(midPointX-point.x()) < 0.01:
            midPointX = point.x()
        if abs(midPointY-point.y()) < 0.01:
            midPointY = point.y()

        # 由逆時針順序判斷點在線的哪邊
        if convexLine[2] == 'left':
            vectorX = point.x()-midPointX
            vectorY = point.y()-midPointY
        elif convexLine[2] == 'right':
            vectorX = midPointX-point.x()
            vectorY = midPointY-point.y()
        else:
            vectorX = 0
            vectorY = 0

        if (point.x()-midPointX) != 0:  # 正常情況
            m = (point.y()-midPointY) / (point.x()-midPointX)
            c = point.y()-(m*point.x())
        else:
            if (point.y()-midPointY) == 0:  # 交點在線上
                m = -(convexLine[0].x1()-convexLine[0].x2()) / \
                      (convexLine[0].y1()-convexLine[0].y2())
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
            if vectorY > 0:  # 垂直
                drawPointY = 600
            elif vectorY < 0:  # 水平
                drawPointY = 0
            else:  # 點在線上
                if convexLine[0].x1()-convexLine[0].x2() > 0 and convexLine[0].y1()-convexLine[0].y2() > 0:
                    drawPointX = 0
                elif convexLine[0].x1()-convexLine[0].x2() > 0 and convexLine[0].y1()-convexLine[0].y2() < 0:
                    drawPointX = 600
                elif convexLine[0].x1()-convexLine[0].x2() < 0 and convexLine[0].y1()-convexLine[0].y2() > 0:
                    drawPointX = 0
                elif convexLine[0].x1()-convexLine[0].x2() < 0 and convexLine[0].y1()-convexLine[0].y2() < 0:
                    drawPointX = 600
                drawPointY = m*drawPointX+c

        if drawPointX != point.x() or drawPointY != point.y():
            self.pen = QtGui.QPen(QtCore.Qt.white)
            eraseLine = QtCore.QLineF(
                point.x(), point.y(), drawPointX, drawPointY)
            self.scene.addLine(eraseLine, self.pen)

            distance1 = self.calculateDistance(
                convexLine[1].x1(), convexLine[1].y1(), drawPointX, drawPointY)
            distance2 = self.calculateDistance(
                convexLine[1].x2(), convexLine[1].y2(), drawPointX, drawPointY)
            if distance1 < distance2:
                convexLine[1].setP1(QtCore.QPointF(point.x(), point.y()))
            else:
                convexLine[1].setP2(QtCore.QPointF(point.x(), point.y()))

            print('Voronoi: ' , convexLine[1])

    def calculateDistance(self, x1, y1, x2, y2):
        return numpy.sqrt(pow(x1-x2, 2) + pow(y1-y2,2))

    def hasDuplicate(self, list):
        temp = []
        for item in list:
            if item not in temp:
                temp.append(item)

        if len(temp) != len(list):
            return True
        else:
            return False
