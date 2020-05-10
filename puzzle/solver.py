# encoding: utf-8
'''
Created on 2020年05月09日
@author: Liang Zehao
@file: solver.py
@description: 八数码搜索算法
'''

'''
状态节点类
'''
class Node:
    '''
    :param data: 表示状态的字符串,由数字1到8以及空格组成, 如'123 45678',表示的棋盘如下:
    1 2 3
      4 5
    6 7 8
    :param cost: 从初始状态结点到此结点的耗费,取值等于结点的深度
    :param parent: 结点的父指针
    '''
    def __init__(self, data, cost = 0, parent = None):
        self.data = data
        self.parent = parent# 指向父亲结点
        self.cost = cost

'''
包含五个搜索算法的八数码求解器类
'''
class Solver:
    def __init__(self, start, target='1238 4765', max_depth=3):
        self.start = start
        self.target = target
        self.max_depth = max_depth
        '''
        self.G保存搜索图,用于查找解路 
        字典类型,保存状态结点, key=状态字符串, value=状态结点
        例如 G= {'1238 4765': Node()}
        '''
        self.G = {}

    def __init__(self, start, **kwargs):
        self.start = start
        self.target = '1238 4765'
        self.max_depth = 3
        if 'target' in kwargs:
            self.target = kwargs['target']
        if 'max_depth' in kwargs:
            self.max_depth = kwargs['max_depth']
        '''
        self.G保存搜索图,用于查找解路 
        字典类型,保存状态结点, key=状态字符串, value=状态结点
        例如 G= {'1238 4765': Node()}
        '''
        self.G = {}

    '''
    状态结点n的后继结点
    用法: 
    for node in succ(n):
        #...
    :param n 状态n
    :yield 生成器每次返回一个后继结点
    '''
    def succ(self, n):
        arr = [char for char in n]
        idx = arr.index(' ')# 空格的索引位置
        # 与四个方向相邻的将牌交换
        if idx not in [2, 5, 8]:
            arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]# 与右方交换位置
            yield ''.join(arr)
            arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]
        if idx not in [0, 3, 6]:
            arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]# 与左方交换位置
            yield ''.join(arr)
            arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]
        if idx < 6:
            arr[idx], arr[idx + 3] = arr[idx + 3], arr[idx]# 与下方交换位置
            yield ''.join(arr)
            arr[idx], arr[idx + 3] = arr[idx + 3], arr[idx]
        if idx > 2:
            arr[idx], arr[idx - 3] = arr[idx - 3], arr[idx]#与上方交换位置
            yield ''.join(arr)
            arr[idx], arr[idx - 3] = arr[idx - 3], arr[idx]# 还原位置

    '''
    :param self.start 初始状态,字符串类型. 格式如:'1234567 8',对应的九宫格如下:
    1 2 3
    4 5 6 
    7   8
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def dfs(self):
        cnt_of_gen = 0# 生成的节点数
        cnt_of_expanded = 0# 被扩展的节点数
        open_list = [self.start]
        close_list = []
        self.G = {self.start:Node(self.start)}# 搜索图
        while open_list:
            n = open_list.pop()
            # 找到解
            if n == self.target:
                return True, cnt_of_gen, cnt_of_expanded
            close_list.append(n)
            # 搜索深度超过限制
            if self.G[n].cost >= self.max_depth:
                continue
            expanded = False
            # 遍历后继状态
            for s in self.succ(n):
                if s not in close_list:
                    # 对结点n进行扩展,搜索图添加s结点
                    self.G[s] = Node(s, self.G[n].cost + 1, self.G[n])
                    # print(s)# debug
                    cnt_of_gen += 1
                    if s == self.target:
                        return True, cnt_of_gen, cnt_of_expanded + 1
                    open_list.append(s)
                    expanded = True
            if expanded:
                cnt_of_expanded += 1
        return False, cnt_of_gen, cnt_of_expanded

    '''
    :param self.start 初始状态,字符串类型. 格式如:'1234567 8',对应的九宫格如下:
    1 2 3
    4 5 6 
    7   8
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def bfs(self):
        cnt_of_gen = 0# 生成的节点数
        cnt_of_expanded = 0# 被扩展的节点数
        open_list = [self.start]
        close_list = []
        self.G = {self.start:Node(self.start)}# 搜索图
        while open_list:
            n = open_list.pop()
            # 找到解
            if n == self.target:
                return True, cnt_of_gen, cnt_of_expanded
            close_list.append(n)
            # 搜索深度超过限制
            if self.G[n].cost >= self.max_depth:
                continue
            expanded = False
            # 遍历后继状态
            for s in self.succ(n):
                # 如果后继结点已经出现过,则考虑修改cost和父指针,不新建结点
                if s not in close_list:
                    # 对结点n进行扩展,搜索图添加s结点
                    self.G[s] = Node(s, self.G[n].cost + 1, self.G[n])
                    # print(s)# debug
                    cnt_of_gen += 1
                    if s == self.target:
                        return True, cnt_of_gen, cnt_of_expanded + 1
                    open_list.insert(0, s)
                    expanded = True
            if expanded:
                cnt_of_expanded += 1
        return False, cnt_of_gen, cnt_of_expanded

    
    '''
    :param self.start 初始状态,字符串类型. 格式如:'1234567 8',对应的九宫格如下:
    1 2 3
    4 5 6 
    7   8
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def h1(self):
        cnt_of_gen = 0# 生成的节点数
        cnt_of_expanded = 0  # 被扩展的节点数
        # TODO 
        return False, cnt_of_gen, cnt_of_expanded

    '''
    :param self.start 初始状态,字符串类型. 格式如:'1234567 8',对应的九宫格如下:
    1 2 3
    4 5 6 
    7   8
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def h2(self):
        cnt_of_gen = 0# 生成的节点数
        cnt_of_expanded = 0  # 被扩展的节点数
        # TODO 
        return False, cnt_of_gen, cnt_of_expanded

    '''
    :param self.start 初始状态,字符串类型. 格式如:'1234567 8',对应的九宫格如下:
    1 2 3
    4 5 6 
    7   8
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def h3(self):
        cnt_of_gen = 0# 生成的节点数
        cnt_of_expanded = 0  # 被扩展的节点数
        # TODO    
        return False, cnt_of_gen, cnt_of_expanded

    '''
    解路生成器,每次迭代返回从解路的下一个状态
    '''
    def ans(self):
        p = self.G[self.target]
        solve = []
        while p:
            solve.append(p.data)
            p = p.parent
        while solve:
            yield solve.pop()

# 本模块的测试入口函数
if __name__ == "__main__":
    s = Solver('2831647 5', max_depth=5)
    flag, cnt_of_gen, cnt_of_expanded = s.dfs()
    print('')
    print('最大搜索深度:', s.max_depth)
    print('找到解:', flag)
    print('生成节点数:', cnt_of_gen)
    print('扩展节点数:', cnt_of_expanded)
    if flag:
        print('逐行打印解路')
        for state in s.ans():
            for i in range(3):
                for j in range(3):
                    print(state[3 * i + j], end=' ')
                print()
            print()


                

 