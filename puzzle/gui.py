# encoding: utf-8
'''
Created on 2020年05月08日
@author: Liang Zehao
@file: gui.py
@description: 八数码实验的图形化界面
'''
import sys
import re
import time
from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout, QHeaderView, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLineEdit,  QMessageBox
from PyQt5.QtGui import QFont, QIcon, QKeySequence, QPixmap
from PyQt5.QtCore import QRect, QSize, QThread, QTimer, Qt, QObject
from solver import Solver
import random

class MyLabel(QPushButton):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setFixedSize(60, 60)

    def input_num(self):
        self.parent.cnt += 1
        self.setText(str(self.parent.cnt))
        self.setEnabled(False)
        if self.parent.cnt == 8:
            # 恢复搜索功能,禁用所有格子可点击
            for btn in self.parent.lbtns:
                btn.setEnabled(True)
            tmp = ''
            for w in self.parent.nums:
                if w.text() == '':
                    w.setText(' ')
                    tmp += ' '
                    w.setEnabled(False)
                else:
                    tmp += w.text()
            self.parent.start = tmp
            self.parent.solver.start = tmp
'''
用于在子线程中对ui进行异步更新
'''
class UpdateObj(QObject):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
    
    def show_ans(self):

        # 解法的动态演示
        for s in self.parent.solver.ans():
            time.sleep(0.3)
            for i, ch in enumerate(s):
                self.parent.nums[i].setText(ch)
        time.sleep(2)
        for i, ch in enumerate(self.parent.start):
            self.parent.nums[i].setText(ch)

'''
八数码图形界面
'''
class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.start = '2 3184765'
        self.cnt = 8# 当前九宫格已经填入的数字的个数
        self.solver = Solver(self.start)
        self.updater = UpdateObj(self)
        self.myThread = QThread()
        self.updater.moveToThread(self.myThread)
        self.initUI()
        self.bindSlots()
        
    '''
    布置所有组件
    '''    
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
        self.setFixedSize(800, 600)
        QLabel('最大搜索深度', self).setGeometry(260, 455, 95, 20)
        self.max_depth = QLineEdit(self)
        self.max_depth.setGeometry(QRect(350, 452, 50, 22))
        self.max_depth.setText(str(self.solver.max_depth))
        
        # 左侧按钮集
        self.lbtns = [
        QPushButton('深度优先搜索', self),
        QPushButton('宽度优先搜索', self),
        QPushButton('启发式搜索1', self),
        QPushButton('启发式搜索2', self),
        QPushButton('启发式搜索3', self),
        QPushButton('全部运行(F5)', self)
        ]
        # 右侧按钮集
        self.rbtns = [
        QPushButton('随机生成', self),
        QPushButton('手动输入', self),
        QPushButton('清空', self),
        QPushButton('退出', self),
        QPushButton('解法演示', self),
        QPushButton('别点', self)
        ]
        # 初始状态禁用
        self.rbtns[4].setEnabled(False)
        self.lbtns[5].setShortcut(QKeySequence("F5"))
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

        # 八数码的牌子设置为初始状态
        self.nums = [MyLabel(self) for _ in range(9)]
        for i, ch in enumerate(self.start):
            self.nums[i].setText(ch)
            self.nums[i].setEnabled(False)
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

    '''
    给必要的控件绑定槽函数
    '''
    def bindSlots(self):
        self.lbtns[0].clicked.connect(self.run_dfs)
        self.lbtns[1].clicked.connect(self.run_bfs)
        self.lbtns[2].clicked.connect(self.run_h1)
        self.lbtns[3].clicked.connect(self.run_h2)
        self.lbtns[4].clicked.connect(self.run_h3)
        self.lbtns[5].clicked.connect(self.run_all)
        self.rbtns[0].clicked.connect(self.random_state)
        self.rbtns[1].clicked.connect(self.manual_input)
        self.rbtns[2].clicked.connect(self.clear)
        self.rbtns[3].clicked.connect(self.close)
        self.rbtns[4].clicked.connect(self.updater.show_ans)
        self.rbtns[5].clicked.connect(self.useless)
        self.max_depth.textChanged[str].connect(self.change_max_depth)
        self.myThread.start()
        for w in self.nums:
            w.clicked.connect(w.input_num)


    def useless(self):
        for _ in range(20):
            QMessageBox.about(self, '叫你别点', '欢迎大家学习人工智能导论')

    def change_max_depth(self, val):
        if re.search('^\\d+$', val):
            self.solver.max_depth = int(val)

    '''
    运行深度优先搜索算法,更新结果表格
    '''        
    def run_dfs(self):
        res, gen, expand = self.solver.dfs()
        self.rbtns[4].setEnabled(True if res else False)  # 是否允许进行解法演示
        print(res, gen, expand)
        self.result.item(0, 1).setText(str(expand))
        self.result.item(1, 1).setText(str(gen))

    '''
    运行宽度优先搜索算法,更新结果表格
    '''
    def run_bfs(self):
        res, gen, expand = self.solver.bfs()
        self.rbtns[4].setEnabled(True if res else False)  # 是否允许进行解法演示
        print(res, gen, expand)
        self.result.item(0, 2).setText(str(expand))
        self.result.item(1, 2).setText(str(gen))

    '''
    运行h1启发式搜索算法,更新结果表格
    '''
    def run_h1(self):
        res, gen, expand = self.solver.h1()
        self.rbtns[4].setEnabled(True if res else False)  # 是否允许进行解法演示
        print(res, gen, expand)
        self.result.item(0, 3).setText(str(expand))
        self.result.item(1, 3).setText(str(gen))

    '''
    运行h2启发式搜索算法,更新结果表格
    '''
    def run_h2(self):
        res, gen, expand = self.solver.h2()
        self.rbtns[4].setEnabled(True if res else False)  # 是否允许进行解法演示
        print(res, gen, expand)
        self.result.item(0, 4).setText(str(expand))
        self.result.item(1, 4).setText(str(gen))
    
    '''
    运行h3启发式搜索算法,更新结果表格
    '''
    def run_h3(self):
        res, gen, expand = self.solver.h3()
        self.rbtns[4].setEnabled(True if res else False)  # 是否允许进行解法演示
        print(res, gen, expand)
        self.result.item(0, 5).setText(str(expand))
        self.result.item(1, 5).setText(str(gen))

    '''
    运行所有搜索算法,更新结果表格
    '''    
    def run_all(self):
        self.run_dfs()
        self.run_bfs()
        self.run_h1()
        self.run_h2()
        self.run_h3()

    '''
    清空结果表
    '''
    def clear(self):
        for i in range(2):
            for j in range(1, 6):
                self.result.item(i, j).setText('')

    '''
    手动输入初始状态
    '''
    def manual_input(self):
        self.clear()# 清空表格
        # 清空九宫格的数字,并设置为可点击,即允许输入
        for w in self.nums:
            w.setText('')
            w.setEnabled(True)
        # 未输入完成前不允许执行搜索和解法演示
        for b in self.lbtns:
            b.setEnabled(False)
        self.rbtns[4].setEnabled(False)
        # 计数器清零
        self.cnt = 0

    ''' 
    生成随机状态
    '''
    def random_state(self):
        self.start = ''.join([str(i) for i in random.sample(range(0, 9), 9)]).replace('0', ' ')
        self.solver.start = self.start
        # 更新ui
        for i, w in enumerate(self.nums):
            w.setText(self.start[i])
        self.rbtns[4].setEnabled(False)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())