from PyQt5 import QtCore, QtGui, QtWidgets
import tkinter as tk
from tkinter import messagebox
import hinh
from nhom_tacgia import *
from guide import *
import turtle
import random

# global move_history
global move_history
global size_board


class Ui_MainWindow(object):
    def nhomtacgia(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow1()
        self.ui.setup(self.window)
        self.window.show()
    def guide(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow2()
        self.ui.setup2(self.window)
        self.window.show()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(877, 574)
        MainWindow.setStyleSheet("background-color: rgb(253, 209, 171);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 20, 911, 131))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 481, 471))
        self.label.setStyleSheet("border-image: url(:/background/img/co-caro-background.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(580, 100, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("background-color: rgb(0, 185, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(start)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(580, 210, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.guide)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(560, 320, 211, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.nhomtacgia)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 877, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GAME CARO"))
        self.pushButton.setText(_translate("MainWindow", "PLAY ????"))
        self.pushButton_2.setText(_translate("MainWindow", " C??CH CH??I ??? "))
        self.pushButton_3.setText(_translate("MainWindow", "NH??M T??C GI???????"))



def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "] * sz)
    return board


def is_empty(board):
    return board == [[' '] * len(board)] * len(board)


def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)


def is_win(board):
    black = score_of_col(board, 'b')
    white = score_of_col(board, 'w')

    sum_sumcol_values(black)
    sum_sumcol_values(white)

    if 5 in black and black[5] == 1:
        return 'Black won'
    elif 5 in white and white[5] == 1:
        return 'White won'

    if sum(black.values()) == black[-1] and sum(white.values()) == white[-1] or possible_moves(board) == []:
        return 'Draw'

    return 'Continue playing'


##AI Engine

def march(board, y, x, dy, dx, length):
    '''
    t??m v??? tr?? xa nh???t trong dy,dx trong kho???ng length

    '''
    yf = y + length * dy
    xf = x + length * dx
    # ch???ng n??o yf,xf kh??ng c?? trong board
    while not is_in(board, yf, xf):
        yf -= dy
        xf -= dx

    return yf, xf


def score_ready(scorecol):
    '''
    Kh???i t???o h??? th???ng ??i???m

    '''
    sumcol = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1

    return sumcol


def sum_sumcol_values(sumcol):
    '''
    h???p nh???t ??i???m c???a m???i h?????ng
    '''

    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())


def score_of_list(lis, col):
    blank = lis.count(' ')
    filled = lis.count(col)

    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled


def row_to_list(board, y, x, dy, dx, yf, xf):
    '''
    tr??? v??? list c???a y,x t??? yf,xf

    '''
    row = []
    while y != yf + dy or x != xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row


def score_of_row(board, cordi, dy, dx, cordf, col):
    '''
    tr??? v??? m???t list v???i m???i ph???n t??? ?????i di???n cho s??? ??i???m c???a 5 kh???i

    '''
    colscores = []
    y, x = cordi
    yf, xf = cordf
    row = row_to_list(board, y, x, dy, dx, yf, xf)
    for start in range(len(row) - 4):
        score = score_of_list(row[start:start + 5], col)
        colscores.append(score)

    return colscores


def score_of_col(board, col):
    '''
    t??nh to??n ??i???m s??? m???i h?????ng c???a column d??ng cho is_win;
    '''

    f = len(board)
    # scores c???a 4 h?????ng ??i
    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
    for start in range(len(board)):
        scores[(0, 1)].extend(score_of_row(board, (start, 0), 0, 1, (start, f - 1), col))
        scores[(1, 0)].extend(score_of_row(board, (0, start), 1, 0, (f - 1, start), col))
        scores[(1, 1)].extend(score_of_row(board, (start, 0), 1, 1, (f - 1, f - 1 - start), col))
        scores[(-1, 1)].extend(score_of_row(board, (start, 0), -1, 1, (0, start), col))

        if start + 1 < len(board):
            scores[(1, 1)].extend(score_of_row(board, (0, start + 1), 1, 1, (f - 2 - start, f - 1), col))
            scores[(-1, 1)].extend(score_of_row(board, (f - 1, start + 1), -1, 1, (start + 1, f - 1), col))

    return score_ready(scores)


def score_of_col_one(board, col, y, x):
    '''
    tr??? l???i ??i???m s??? c???a column trong y,x theo 4 h?????ng,
    key: ??i???m s??? kh???i ????n v??? ???? -> ch??? ktra 5 kh???i thay v?? to??n b???
    '''

    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}

    scores[(0, 1)].extend(score_of_row(board, march(board, y, x, 0, -1, 4), 0, 1, march(board, y, x, 0, 1, 4), col))

    scores[(1, 0)].extend(score_of_row(board, march(board, y, x, -1, 0, 4), 1, 0, march(board, y, x, 1, 0, 4), col))

    scores[(1, 1)].extend(score_of_row(board, march(board, y, x, -1, -1, 4), 1, 1, march(board, y, x, 1, 1, 4), col))

    scores[(-1, 1)].extend(score_of_row(board, march(board, y, x, -1, 1, 4), 1, -1, march(board, y, x, 1, -1, 4), col))

    return score_ready(scores)


def possible_moves(board):
    '''
    kh???i t???o danh s??ch t???a ????? c?? th??? c?? t???i danh gi???i c??c n??i ???? ????nh ph???m vi 3 ????n v???
    '''
    # m???ng taken l??u gi?? tr??? c???a ng?????i ch??i v?? c???a m??y tr??n b??n c???
    taken = []
    # m???ng directions l??u h?????ng ??i (8 h?????ng)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    # cord: l??u c??c v??? tr?? kh??ng ??i
    cord = {}

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i, j))
    ''' duy???t trong h?????ng ??i v?? m???ng gi?? tr??? tr??n b??n c??? c???a ng?????i ch??i v?? m??y, ki???m tra n?????c kh??ng th??? ??i(tr??ng v???i 
    n?????c ???? c?? tr??n b??n c???)
    '''
    for direction in directions:
        dy, dx = direction
        for coord in taken:
            y, x = coord
            for length in [1, 2, 3, 4]:
                move = march(board, y, x, dy, dx, length)
                if move not in taken and move not in cord:
                    cord[move] = False
    return cord


def TF34score(score3, score4):
    '''
    tr??? l???i tr?????ng h???p ch???c ch???n c?? th??? th???ng(4 ?? li??n ti???p)
    '''
    for key4 in score4:
        if score4[key4] >= 1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >= 2:
                    return True
    return False


def stupid_score(board, col, anticol, y, x):
    '''
    c??? g???ng di chuy???n y,x
    tr??? v??? ??i???m s??? t?????ng tr??ng l???i th???
    '''

    global colors
    M = 1000
    res, adv, dis = 0, 0, 0

    # t???n c??ng
    board[y][x] = col
    # draw_stone(x,y,colors[col])
    sumcol = score_of_col_one(board, col, y, x)
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    # {0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    adv += sumcol[-1] + sumcol[1] + 4 * sumcol[2] + 8 * sumcol[3] + 16 * sumcol[4]

    # ph??ng th???
    board[y][x] = anticol
    sumanticol = score_of_col_one(board, anticol, y, x)
    d = winning_situation(sumanticol)
    dis += d * (M - 100)
    sum_sumcol_values(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4 * sumanticol[2] + 8 * sumanticol[3] + 16 * sumanticol[4]

    res = adv + dis

    board[y][x] = ' '
    return res


def winning_situation(sumcol):
    '''
    tr??? l???i t??nh hu???ng chi???n th???ng d???ng nh??:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 l??u ??i???m c?? ????? nguy hi???m t??? th???p ?????n cao,
    -1 l?? r??i v??o tr???ng th??i t???i, c???n ph??ng th???
    '''

    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4]) >= 2 or (len(sumcol[4]) >= 1 and max(sumcol[4].values()) >= 2):
        return 4
    elif TF34score(sumcol[3], sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(), reverse=True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0


def best_move(board, col):
    '''
    tr??? l???i ??i???m s??? c???a m???ng trong l???i th??? c???a t???ng m??u
    '''
    if col == 'w':
        anticol = 'b'
    else:
        anticol = 'w'

    movecol = (0, 0)
    maxscorecol = ''
    # ki???m tra n???u b??n c??? r???ng th?? cho v??? tr?? random n???u kh??ng th?? ????a ra gi?? tr??? tr??n b??n c??? n??n ??i
    if is_empty(board):
        movecol = (int((len(board)) * random.random()), int((len(board[0])) * random.random()))
    else:
        moves = possible_moves(board)

        for move in moves:
            y, x = move
            if maxscorecol == '':
                scorecol = stupid_score(board, col, anticol, y, x)
                maxscorecol = scorecol
                movecol = move
            else:
                scorecol = stupid_score(board, col, anticol, y, x)
                if scorecol > maxscorecol:
                    maxscorecol = scorecol
                    movecol = move
    return movecol


##Graphics Engine

def click(x, y):
    global board, colors, win, move_history

    x, y = getindexposition(x, y)

    if x == -1 and y == -1 and len(move_history) != 0:
        x, y = move_history[-1]

        del (move_history[-1])
        board[y][x] = " "
        x, y = move_history[-1]

        del (move_history[-1])
        board[y][x] = " "
        return

    if not is_in(board, y, x):
        return

    if board[y][x] == ' ':

        draw_stone(x, y, colors['b'])
        board[y][x] = 'b'

        move_history.append((x, y))

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            root = tk.Tk()
            MsgBox = tk.messagebox.askquestion(
                title='Th??ng b??o',
                message=game_res
            )
            root.destroy()
            if MsgBox == 'yes':
                # turtle.exitonclick()
                root.mainloop()
            elif MsgBox == 'no':
                root.mainloop()
            win = True
            return

        ay, ax = best_move(board, 'w')
        draw_stone(ax, ay, colors['w'])
        board[ay][ax] = 'w'

        move_history.append((ax, ay))

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            root = tk.Tk()
            MsgBox = tk.messagebox.askquestion(
                title='Th??ng b??o',
                message=game_res
            )
            root.destroy()
            if MsgBox == 'yes':
                root.mainloop()
            elif MsgBox == 'no':
                root.mainloop()
            win = True
            return


def initialize(size):
    global win, board, screen, colors, move_history

    move_history = []
    win = False
    board = make_empty_board(size)

    screen = turtle.Screen()
    screen.onclick(click)
    screen.setup(screen.screensize()[1] * 2, screen.screensize()[1] * 2)
    screen.setworldcoordinates(-1, size, size, -1)
    screen.bgcolor('orange')
    screen.tracer(500)

    colors = {'w': turtle.Turtle(), 'b': turtle.Turtle(), 'g': turtle.Turtle()}
    colors['w'].color('white')
    colors['b'].color('black')

    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)

    border = turtle.Turtle()
    border.speed(9)
    border.penup()

    side = (size - 1) / 2

    i = -1
    for start in range(size):
        border.goto(start, side + side * i)
        border.pendown()
        i *= -1
        border.goto(start, side + side * i)
        border.penup()

    i = 1
    for start in range(size):
        border.goto(side + side * i, start)
        border.pendown()
        i *= -1
        border.goto(side + side * i, start)
        border.penup()

    border.ht()

    screen.listen()
    screen.mainloop()


def getindexposition(x, y):
    '''
    l???y index
    '''
    intx, inty = int(x), int(y)
    dx, dy = x - intx, y - inty
    if dx > 0.5:
        x = intx + 1
    elif dx < -0.5:
        x = intx - 1
    else:
        x = intx
    if dy > 0.5:
        y = inty + 1
    elif dx < -0.5:
        y = inty - 1
    else:
        y = inty
    return x, y


def draw_stone(x, y, colturtle):
    colturtle.goto(x, y - 0.4)
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle(0.45)
    colturtle.end_fill()
    colturtle.penup()


def start():
    initialize(30)
    turtle.bye()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
