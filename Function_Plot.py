import numpy as np
from sympy import *
from PySide2.QtWidgets import *
import pyqtgraph as pg
import sys
from PySide2.QtGui import QIcon, QPixmap, QFont
from array import array

#pyside2 & pyqtgraph

class Window (QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle ('Graphic Calculator')
        self.setGeometry(50,50,300,200)
        self.setIconMode()
        self.Create_TextBox()
        self.Center()


    def Create_TextBox(self):
        self.FuncTextBox = QLineEdit(self)
        self.FuncTextBox.setFixedWidth(140)
        self.FuncTextBox.cursor()
        self.FuncTextBox.move(90, 50)
        self.FuncTextBox.setPlaceholderText('Enter a Function F(x)')
        self.FuncTextBox1 = QLabel('Function: ',self)
        self.FuncTextBox1.move(25,52)

        self.Xmin = QLineEdit(self)
        self.Xmin.setFixedWidth(90)
        self.Xmin.cursor()
        self.Xmin.move(90, 80)
        self.Xmin.setPlaceholderText('Enter X_min')
        self.FuncTextBox1 = QLabel('X Minimum: ', self)
        self.FuncTextBox1.move(12, 82)


        self.Xmax = QLineEdit(self)
        self.Xmax.setFixedWidth(90)
        self.Xmax.cursor()
        self.Xmax.move(90, 110)
        self.Xmax.setPlaceholderText('Enter X_max')
        self.FuncTextBox1 = QLabel('X Maximum: ', self)
        self.FuncTextBox1.move(10, 112)



        self.PlotButton = QPushButton('Plot The Function', self)
        self.PlotButton.move(80, 140)
        #self.PlotButton.clicked.connect(self.menubar)
        self.PlotButton.clicked.connect(self.PopUp)


        self.show()

    def PopUp(self):

        Function = self.FuncTextBox.text().lower()
        X_Min = self.Xmin.text()
        X_Max = self.Xmax.text()

        # Errors detection
        for j in range(len(Function)):
            # 1) x***2
            if (Function[j] == '*') and (j + 1 < len(Function)):
                if (j + 2 < len(Function)) and (Function[j + 1] == '*'):
                    if (Function[j + 2] == '*'):
                        msg = QMessageBox()
                        msg.setWindowTitle('Error')
                        msg.setText('ERROR!, Incorrect syntax *** is undefined')
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                        exit()

            # 2) 3++2 , 3--x 'Two similar signs back to back'
            if (Function[j] in ('+', '-', '/', '^')) and (j + 1 < len(Function)):
                if Function[j] == Function[j + 1]:
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Incorrect Syntax')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            if (Function[j] == '*') and (j + 1 < len(Function)):
                if (j + 2 >= len(Function)) and (Function[j + 1] == '*'):
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Incorrect Syntax')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            # 3) 3+-2 , x */ 5 'Two diff signs back to back'

            if ((Function[j] == '+') and (j + 1 < len(Function))):
                if (Function[j + 1] in ('-', '*', '/', '^')):
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Incorrect Syntax')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            if ((Function[j] == '-') and (j + 1 < len(Function))):
                if (Function[j + 1] in ('+', '*', '/', '^')):
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Incorrect Syntax')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            if ((Function[j] == '*') and (j + 1 < len(Function))):
                if (Function[j + 1] in ('+', '-', '/', '^')):
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Incorrect Syntax')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            if ((Function[j] == '/') and (j + 1 < len(Function))):
                if (Function[j + 1] in ('+', '*', '-', '^')):
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Incorrect Syntax')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            if ((Function[j] == '^') and (j + 1 < len(Function))):
                if (Function[j + 1] in ('+', '*', '/', '-')):
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Incorrect Syntax')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            # 4) 3+ -4 , 3* *4 'Two diff/similar sign seprated by space'
            if Function[j] in ('+', '-', '*', '/', '^') and (j + 1 < len(Function)):

                if (Function[j + 1] == ' ') and (j + 2 < len(Function)):

                    if Function[j] == Function[j + 2]:
                        msg = QMessageBox()
                        msg.setWindowTitle('Error')
                        msg.setText('Error! Incorrect Syntax')
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                        exit()

                    elif ((Function[j] == '+') and (Function[j + 2] in ('-', '*', '/', '^'))) or (
                            (Function[j] == '-') and (Function[j + 2] in ('+', '', '/', '^'))) or (
                            (Function[j] == '') and (Function[j + 2] in ('-', '+', '/', '^'))) or (
                            (Function[j] == '/') and (Function[j + 2] in ('-', '', '+', '^'))) or (
                            (Function[j] == '^') and (Function[j + 2] in ('-', '*', '/', '+'))):
                        msg = QMessageBox()
                        msg.setWindowTitle('Error')
                        msg.setText('Error! Incorrect Syntax')
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                        exit()
            # 5) a+3*x
            if Function[j].lower() in (
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v',
                    'w', 'y', 'z'):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! Please make sure the equation is function in x ONLY')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()
            # 6) xx
            if (Function[j].lower() == 'x') and (j + 1 < len(Function)):
                if Function[j + 1].lower() == 'x':
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Missing an operator, ')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            # 7) $, %, @,)
            if Function[j] not in (
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x', 'X', '+', '-', '*', '/', '^', ' ', '(', ')'):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! Not allowed character was entered')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()

            # 8) + , -  'starting or ending with operator or any unknown character'
            if (Function[j].lower() not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x', ')')) and (
                    j + 1 >= len(Function)):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! : incomplete function ')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()

            if (Function[j].lower() not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x', '(')) and (
                    j - 1 < 0):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! : incomplete function ')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()

            # 9)  3x  or x3

            if (Function[j].lower() == 'x') and (j - 1 >= 0):
                if Function[j - 1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! an operator is missing')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            if (Function[j].lower() == 'x') and (j + 1 < len(Function)):
                if Function[j + 1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! an operator is missing')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            # 10) many spaces between operators or incorrect character
            if Function[j] in ('+', '-', '*', '/', '^') and (j + 1 < len(Function)):
                if (Function[j + 1] == ' ') and (j + 2 < len(Function)):
                    if (Function[j + 2].lower() not in (
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x', '(', ')')):
                        msg = QMessageBox()
                        msg.setWindowTitle('Error')
                        msg.setText('Wrong Logic, might be too many spaces between the operators')
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                        exit()

            if Function[j] in ('+', '-', '*', '/', '^') and (j - 1 >= 0):
                if (Function[j - 1] == ' ') and (j - 2 > 0):
                    if (Function[j - 2].lower() not in (
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x', '(', ')')):
                        msg = QMessageBox()
                        msg.setWindowTitle('Error')
                        msg.setText('Wrong Logic, might be too many spaces between the operators')
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                        exit()

            # 11) divide by zero

            if (Function[j] == '/') and (j + 1 < len(Function)):
                if Function[j + 1] == '0':
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Dividing by zero')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()

            if (Function[j] == '/') and (j + 2 < len(Function)):
                if Function[j + 1] == ' ' and Function[j + 2] == '0':
                    msg = QMessageBox()
                    msg.setWindowTitle('Error')
                    msg.setText('Error! Dividing by zero')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    exit()


            # 12) Brackets Check and handeling

        Counter_open = 0
        Counter_close = 0

        for h in range(len(Function)):
            if Function[h] == '(':
                Counter_open += 1

        for f in range(len(Function)):
            if Function[f] == ')':
                Counter_close += 1

        if ((Counter_open > 0) and (Counter_close == 0)) or ((Counter_close > 0) and (Counter_open == 0)):
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Error! Missing bracket/s')
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            exit()
        elif ((Counter_open > 0) and (Counter_close > 0)):
            if Counter_open != Counter_close:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! Missing bracket/s')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()

            # 13) Xmin and Xmax Check

        for n in range(len(X_Min)):
            if X_Min[n] not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9','-','.'):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! X Minimum must be a number')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()

            if (X_Min[n] == '.') and (n + 1 >= len(X_Min)):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! : Incomplete function ')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()

            if (X_Min[n] == '.') and (n - 1 < 0):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! : Incomplete function ')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()




        for m in range(len(X_Max)):
            if X_Max[m] not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9','-','.'):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! X Maximum must be a number ')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()

            if (X_Max[m] == '.') and (m + 1 >= len(X_Max)):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! : Incomplete function ')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()

            if (X_Max[m] == '.') and (m - 1 < 0):
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Error! : Incomplete function ')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                exit()


        #14) Xmax < Xmin

        min_X = sympify(X_Min)
        max_X = sympify(X_Max)

        if ((min_X) > (max_X))  :
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Error! X Minimum must be greater than X Maximum ')
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            exit()


        expr = sympify(Function)

        X_range = np.arange(float(X_Min), float(X_Max), 0.1)
        X_Range = []
        X_Range = X_range

        x = Symbol('x')

        Y_range = array('d')

        for i in range(len(X_range)):
            Y_axis = expr.subs(x, X_range[i])
            Y_range.append(Y_axis)

        #PLOT

        plotGraph = pg.plot(title='Graph Figure')
        plotGraph.plot(X_Range,Y_range)



    def menubar(self):
        func = self.FuncTextBox.text()
        # xmin = self.Xmin.text()
        # xmax = self.Xmax.text()

        self.setWindowTitle('Processing the function : ' + func)

    def setIconMode (self):
        icon1 = QIcon ('plot icon.png')
        label1 = QLabel ('Sample' , self)
        pixmap1 = icon1.pixmap (45,45,QIcon.Active , QIcon.On)
        label1.setPixmap(pixmap1)
        label1.move(2,4)
        label1.setToolTip('Graphic Calculator')

    def Center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())


myApp = QApplication(sys.argv)
Window = Window()
Window.show()
myApp.exec_()