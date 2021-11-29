from PyQt5 import QtCore, QtGui, QtWidgets
import turtle
import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

global move_history
global size_board

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(877, 574)
        MainWindow.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 20, 911, 131))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 481, 471))
        self.label.setStyleSheet("border-image: url(:/background /co-caro-background.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(580, 60, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(start)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(580, 140, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(560, 400, 211, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(570, 270, 71, 61))
        self.label_3.setStyleSheet("border-image: url(:/background /white.png);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(670, 270, 71, 61))
        self.label_4.setStyleSheet("border-image: url(:/background /black.png);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(550, 230, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.label_5.setObjectName("label_5")
        self.checkBoxW = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxW.setGeometry(QtCore.QRect(590, 350, 71, 20))
        self.checkBoxW.setText("")
        self.checkBoxW.setObjectName("checkBoxW")
        self.checkBoxB = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxB.setGeometry(QtCore.QRect(700, 350, 71, 20))
        self.checkBoxB.setText("")
        self.checkBoxB.setObjectName("checkBoxB")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PLAY"))
        self.pushButton_2.setText(_translate("MainWindow", "CÁCH CHƠI"))
        self.pushButton_3.setText(_translate("MainWindow", "NHÓM TÁC GIẢ"))
        self.label_5.setText(_translate("MainWindow", "         Chọn quân"))

import turtle
import random
import time

global move_history


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
    tìm vị trí xa nhất trong dy,dx trong khoảng length

    '''
    yf = y + length * dy
    xf = x + length * dx
    # chừng nào yf,xf không có trong board
    while not is_in(board, yf, xf):
        yf -= dy
        xf -= dx

    return yf, xf


def score_ready(scorecol):
    '''
    Khởi tạo hệ thống điểm

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
    hợp nhất điểm của mỗi hướng
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
    trả về list của y,x từ yf,xf

    '''
    row = []
    while y != yf + dy or x != xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row


def score_of_row(board, cordi, dy, dx, cordf, col):
    '''
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

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
    tính toán điểm số mỗi hướng của column dùng cho is_win;
    '''

    f = len(board)
    # scores của 4 hướng đi
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
    trả lại điểm số của column trong y,x theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    '''

    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}

    scores[(0, 1)].extend(score_of_row(board, march(board, y, x, 0, -1, 4), 0, 1, march(board, y, x, 0, 1, 4), col))

    scores[(1, 0)].extend(score_of_row(board, march(board, y, x, -1, 0, 4), 1, 0, march(board, y, x, 1, 0, 4), col))

    scores[(1, 1)].extend(score_of_row(board, march(board, y, x, -1, -1, 4), 1, 1, march(board, y, x, 1, 1, 4), col))

    scores[(-1, 1)].extend(score_of_row(board, march(board, y, x, -1, 1, 4), 1, -1, march(board, y, x, 1, -1, 4), col))

    return score_ready(scores)


def possible_moves(board):
    '''
    khởi tạo danh sách tọa độ có thể có tại danh giới các nơi đã đánh phạm vi 3 đơn vị
    '''
    # mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    # cord: lưu các vị trí không đi
    cord = {}

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i, j))
    ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
    nước đã có trên bàn cờ)
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
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    '''
    for key4 in score4:
        if score4[key4] >= 1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >= 2:
                    return True
    return False


def stupid_score(board, col, anticol, y, x):
    '''
    cố gắng di chuyển y,x
    trả về điểm số tượng trưng lợi thế
    '''

    global colors
    M = 1000
    res, adv, dis = 0, 0, 0

    # tấn công
    board[y][x] = col
    # draw_stone(x,y,colors[col])
    sumcol = score_of_col_one(board, col, y, x)
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    # {0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    adv += sumcol[-1] + sumcol[1] + 4 * sumcol[2] + 8 * sumcol[3] + 16 * sumcol[4]

    # phòng thủ
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
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
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
    trả lại điểm số của mảng trong lợi thế của từng màu
    '''
    if col == 'w':
        anticol = 'b'
    else:
        anticol = 'w'

    movecol = (0, 0)
    maxscorecol = ''
    # kiểm tra nếu bàn cờ rỗng thì cho vị trí random nếu không thì đưa ra giá trị trên bàn cờ nên đi
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
                title='Thông báo',
                message=game_res
            )
            root.destroy()
            if MsgBox == 'yes':
                turtle.exitonclick()
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
                title='Thông báo',
                message=game_res
            )
            root.destroy()
            if MsgBox == 'yes':
                turtle.exitonclick()
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
    lấy index
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
    colturtle.goto(x, y - 0.3)
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle(0.3)
    colturtle.end_fill()
    colturtle.penup()


def start():
    initialize(30)
    MainWindow.hide()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
