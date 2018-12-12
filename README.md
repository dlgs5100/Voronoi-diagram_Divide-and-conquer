# 高等演算法設計與分析(Design and Analysis of Algorithms) Term Project : Voronoi diagram with divide and conquer

## Identification:
系級: 資工碩一 </br>
學號: M073040009 </br>
姓名: 鄭詠鴻 </br>

---
## Introduction:
Voronoi diagram(沃羅諾伊圖)又稱為Dirichlet tessellation，是由俄國數學家格奧爾吉·沃羅諾伊建立的空間分割算法，透過視覺化圖形表現出所有點的勢力範圍。 </br>
其中的點和邊包含了幾項意義: </br>
1. Voronoi多邊形上的所有點和相鄰的多邊形生成元的距離相同。
2. 透過1可知，若點在該生成元之範圍內，則該點距離此生成元相較於其他生成元近。

因此常被運用於地理、氣象、機器人...等，各式各樣領域。 </br>

## Method:
Voronoi diagram並非新的問題，現今也存在許多種解法。
1. Half plane intersection
2. Incremental method
3. Divide and conquer
4. Fortune's Algorithm

而此程式則採用第三種Divide and conquer作法實作。 </br>

## Implementation:
### Divide:
1. 以Recursive方式將點分至最多為3，最少為2的subproblem。
2. 找出各個subproblem之convex hull(邊的向量設定為逆時針)。
3. 透過convex hull找出perpendicular bisector，若三點則找出外心，並更新perpendicular bisector。
### Merge:
1. 以右邊subproblem的所有點，依序判斷左邊的所有線，當右邊點是在左邊線的right，則更新左邊的convex hull連至該點。最後找出最下方之外公切線，並將其他方才連至右邊新點之線設為inner convex hull，並捨棄。
2. 以左邊subproblem的所有點，依序判斷右邊的所有線，類推1，找出最上方之外公切線。
3. 透過最上方之外公切線，以此垂直畫出第一條hyperplane。
4. 當hyperplane碰到左邊perpendicular bisector，則畫一輔助線，輔助線為方才右點連至左邊convex hull的inner point;反之，碰到右邊perpendicular bisector，則輔助線為左點連右邊convex hull的inner point，並更新碰到的perpendicular bisector。
5. 重複4，直到碰到最下方外公切線。

## Specification:
### Input:
1. 手動輸入X、Y座標
2. 點擊畫布
3. 讀檔
    ```
    #n              #n為自然數或0，表示此組測驗中會有n個點的輸入
    #x_1 y_1        #n之下會有n行資料、分別表示點的x、y座標資料
    #x_2 y_2        #畫布左上角為座標(0,0)、右下角為(600,600)
    #x_3 y_3        #畫布大小可自行調整、但我們輸入的座標值會在[0,600]之間
    #               #
    #.....          #若為0時，則表示此測試檔案已無其它待測資料、可結束程式
    #               #
    #x_n y_n        #除說明事項外，輸入資料為error free、可不用另外做檢查
    ```
### Output:
```
輸入的座標點：P x y       // 每個點佔一行，兩整數 x, y 為座標。
線段：E x1 y1 x2 y2      // (x1, y1) 為起點，(x2, y2) 為終點，其中 x1≦x2 或 x1=x2, y1≦y2
```
### Feature:
1. Run
2. Step by step

## Programming:
### Data structure:
- Python List
- PYQT QPoint
    ```
    __init__ (self)
    __init__ (self, int xpos, int ypos)
    __init__ (self, QPoint)
    bool isNull (self)
    int manhattanLength (self)
    setX (self, int xpos)
    setY (self, int ypos)
    int x (self)
    int y (self)
    ```
- PYQT QLine
    ```
    __init__ (self)
    __init__ (self, QPoint pt1_, QPoint pt2_)
    __init__ (self, int x1pos, int y1pos, int x2pos, int y2pos)
    __init__ (self, QLine)
    int dx (self)
    int dy (self)
    bool isNull (self)
    QPoint p1 (self)
    QPoint p2 (self)
    setLine (self, int aX1, int aY1, int aX2, int aY2)
    setP1 (self, QPoint aP1)
    setP2 (self, QPoint aP2)
    setPoints (self, QPoint aP1, QPoint aP2)
    translate (self, QPoint point)
    translate (self, int adx, int ady)
    QLine translated (self, QPoint p)
    QLine translated (self, int adx, int ady)
    int x1 (self)
    int x2 (self)
    int y1 (self)
    int y2 (self)
    ```
### Layout:
- PYQT QMainWindow
- PYQT QDialog
- PYQT QGraphicsView
- PYQT QPushButton
- PYQT QLabel
- PYQT QLineEdit
### Control:
- PYQT pyqt5.uic.loadui
- PYQT QtCore.pyqtSignal

## Manual:
- 務必將.exe檔以及.ui檔放在相同資料夾。
- 使用Step by step功能時，請先使用Run執行一次。
- 若輸入測資時畫布上仍有上筆資料，請按Clear鍵。
- 讀檔多筆測資時，欲顯示下筆測資，請按Run鍵。

## Experimental Result:
### Environment:
- OS: Windows 10
- CPU: Intel(R) Xeon(R) CPU E3-1230 V2
- RAM: 8G
- Compiler: Python 3
### Discussion
未達成
1. 在merge Convex hull的時間複雜度在worst case會到O(n^2)，無法達到O(n)。
2. 在Hyperplane由於事前的sort，導致average case會到O(n^2)，無法達到O(n)。
3. Divide and conquer由於資料結構設計不夠完善，無法執行超過6點。
4. Subproblem間有三點以上共線，在merge上會發生錯誤。
5. 在畫Hyperplane部分，由於只判斷Convex hull之y座標，因此有些情況會發生錯誤。
6. 在Hyperplane清除部分，僅在碰到中垂線才觸發清除，因此若沒碰到該須清除中垂線，將發生錯誤。

## Conclusion:
這次的Project不僅僅是理解不容易，在實作方面更是困難重重。由於以往都是習慣理解後自行實作資料結構及演算法，但經過此次作業後了解到，好的Data Structure及Algorithm的重要性。

---
## License and copyright
© Jerry Cheng
