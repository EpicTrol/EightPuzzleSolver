# encoding: utf-8
'''
Created on 2020年05月08日
@author: Liang Zehao
@file: gui.py
@description: 八数码实验的图形化界面
'''
import sys
from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout, QHeaderView, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import QRect, QSize, Qt
from solver import Solver
import random
'''
八数码图形界面
'''
class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.start = '1234 5678'
        self.solver = Solver()
        self.initUI()
        self.bindSlots()
        
        
    def initUI(self):
        with open('./style.qss', encoding='utf8', mode='r') as f:
            self.qss = f.read()
        self.setStyleSheet(self.qss)# 应用qss样式表
        self.setWindowTitle('八数码实验')
        self.setWindowIcon(QIcon('8puzzle.png'))  # 设置应用图标

        self.title = QLabel('八数码问题的实验程序', self)
        self.title.setObjectName('title')
        self.title.move(78, 52)
        self.setGeometry(300, 300, 800, 600)

        # 左侧按钮集
        self.lbtns = [
        QPushButton('深度优先搜索', self),
        QPushButton('宽度优先搜索', self),
        QPushButton('启发式搜索1', self),
        QPushButton('启发式搜索2', self),
        QPushButton('启发式搜索3', self),
        QPushButton('全部运行', self)
        ]
        # 右侧按钮集
        self.rbtns = [
        QPushButton('随机生成', self),
        QPushButton('手动输入', self),
        QPushButton('清空', self),
        QPushButton('回退', self),
        QPushButton('解法演示', self),
        QPushButton('开始游戏', self)
        ]
        # 分别将两侧按钮集添加到两个垂直布局中
        self.ver_layout1 = QVBoxLayout()
        self.ver_layout2 = QVBoxLayout()
        for btn in self.lbtns:
            self.ver_layout1.addWidget(btn)
        for btn in self.rbtns:
            self.ver_layout2.addWidget(btn)
        # 调整按钮栏的位置
        self.ver_layout1.setGeometry(QRect(87, 135, 140, 320))
        self.ver_layout2.setGeometry(QRect(572, 135, 140, 320))

        # 八数码值标签的初始化
        self.nums = [QLabel(self) for _ in range(9)]
        for i, ch in enumerate(self.start):
            self.nums[i].setAlignment(Qt.AlignCenter|Qt.AlignVCenter)# 设置文本居中
            self.nums[i].setText(ch)
        # 八数码棋盘
        self.puzzles = QFrame(self)
        self.puzzles.setObjectName('puzzles')
        self.puzzles.setGeometry(QRect(310, 135, 210, 210))
        # 设置八数码的九宫格显示
        grid = QGridLayout(self.puzzles)
        positions = [(i, j) for i in range(3) for j in range(3)]
        for label, position in zip(self.nums, positions):
            grid.addWidget(label, *position)
        # 构建结果表格
        self.result = QTableWidget(2, 6, self)
        self.result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)# 设置自适应列宽
        self.result.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result.setHorizontalHeaderLabels(['方法', '深度优先', '宽度优先', 'h1(n)', 'h2(n)', 'h3(n)'])
        for i in range(2):
            for j in range(6):
                self.result.setItem(i, j, QTableWidgetItem())# 添加item
                self.result.item(i, j).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 设置文本居中
        self.result.item(0,0).setText('扩展节点数')
        self.result.item(1,0).setText('生成节点数')
        self.result.setGeometry(QRect(87, 478, 630, 100))# 调整表格位置
        # 设置logo
        self.logo = QLabel(self)
        self.logo.setGeometry(QRect(600, 10, 90, 100))
        jpg = QPixmap('scnulogo.png').scaled(self.logo.width(), self.logo.height())
        self.logo.setPixmap(jpg)
        # 增添提示
        self.descrip = QLabel(self)
        self.descrip.setGeometry(QRect(260, 360, 300, 100))
        self.descrip.setText('''手动输入的方法:陆续点击网格未确定的格子,\n依次填入数字1, 2 , 3, 4, 5, 6, 7, 8\nh1(n) =W(n) “不在位”的将牌数\nh2(n) = P(n)将牌“不在位”的距离和\nh3(n) = h(n)＝P(n)+3S(n)''')
        self.show()

    def bindSlots(self):
        self.lbtns[0].clicked[bool].connect(self.run_dfs)
        self.rbtns[0].clicked[bool].connect(self.random_state)
        
    def run_dfs(self):
        res, gen, expand = self.solver.dfs(self.start)
        print(res, gen, expand)
        self.result.item(0, 1).setText(str(expand))
        self.result.item(1, 1).setText(str(gen))
    ''' 
    生成随机状态
    '''
    def random_state(self):
        self.start = ''.join([str(i) for i in random.sample(range(0, 9), 9)]).replace('0', ' ')
        for i, w in enumerate(self.nums):
            w.setText(self.start[i])
    '''
    更新状态
    '''
    def updateGrid(self):
        pass


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())