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
    def __init__(self, data, cost = 0, parent = None, **kwargs):
        self.data = data
        self.parent = parent# 指向父亲结点
        self.cost = cost
        if 'f' in kwargs:
            self.f = kwargs['f']
        else:
            self.f = cost

'''
包含五个搜索算法的八数码求解器类
'''
class Solver:
    def __init__(self, start, target='1238 4765', max_depth=9):
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
        if 'target' in kwargs:
            self.target = kwargs['target']
        if 'max_depth' in kwargs:
            self.max_depth = kwargs['max_depth']
        else:
            self.max_depth = 9#默认值
        '''
        self.G保存搜索图,用于查找解路 
        字典类型,保存状态结点, key=状态字符串, value=状态结点
        例如 G= {'1238 4765': Node()}
        '''
        self.G = {}

    '''
    状态结点n的后继结点的生成器
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
        if idx < 6:
            arr[idx], arr[idx + 3] = arr[idx + 3], arr[idx]# 与下方交换位置
            yield ''.join(arr)
            arr[idx], arr[idx + 3] = arr[idx + 3], arr[idx]
        if idx > 2:
            arr[idx], arr[idx - 3] = arr[idx - 3], arr[idx]#与上方交换位置
            yield ''.join(arr)
            arr[idx], arr[idx - 3] = arr[idx - 3], arr[idx]# 还原位置
        if idx not in [2, 5, 8]:
            arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]# 与右方交换位置
            yield ''.join(arr)
            arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]
        if idx not in [0, 3, 6]:
            arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]# 与左方交换位置
            yield ''.join(arr)
            arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]

    '''
    :param self.start 初始状态,字符串类型. 格式如:'1234567 8',对应的九宫格如下:
    1 2 3
    4 5 6 
    7   8
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def dfs(self):
        cnt_of_gen = 1# 生成的节点数
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
                if s not in self.G:
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
        cnt_of_gen = 1# 生成的节点数
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
                if s not in self.G:
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
    使用了h1评价函数的启发式搜索算法(Heuristic Search)
    :param self.start 初始状态,字符串类型. 格式如:'1234567 8',对应的九宫格如下:
    1 2 3
    4 5 6 
    7   8
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def hs1(self):
        return self.Astar(self.h1)

    '''
    使用了h2评价函数的启发式搜索算法(Heuristic Search)
    :param self.start 初始状态,字符串类型. 格式如:'1234567 8',对应的九宫格如下:
    1 2 3
    4 5 6 
    7   8
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def hs2(self):
        return self.Astar(self.h2)

    '''
    使用了h3评价函数的启发式搜索算法(Heuristic Search)
    :param self.start 初始状态,字符串类型. 格式如:'1234567 8',对应的九宫格如下:
    1 2 3
    4 5 6 
    7   8
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def hs3(self):
        return self.Astar(self.h3)

    '''
    启发式搜索A*算法框架
    :param h: h是一个启发函数,h传入一个状态字符串,返回一个int值,表示启发评分
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def Astar(self, h):
        cnt_of_gen = 1# 生成的节点数
        cnt_of_expanded = 0# 被扩展的节点数
        open_list = [self.start]
        close_list = []
        self.G = {self.start:Node(self.start, 0, f = h(self.start))}# 搜索图
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
                if s in open_list:
                    # 评价函数
                    f = self.G[n].cost + 1 + h(s)
                    if f < self.G[s].f:
                        self.G[s].cost = self.G[n].cost + 1
                        self.G[s].f = f
                        self.G[s].parent = self.G[n]
                elif s in close_list:
                    f = self.G[n].cost + 1 + h(s)
                    # 评价函数值更低,更新父指针
                    if f < self.G[s].f:
                        # fixme
                        self.G[s].cost = self.G[n].cost + 1
                        self.G[s].f = f
                        self.G[s].parent = self.G[n]
                        # 可能后继结点的指针需要修改,将它们加到open表中
                        for child in self.succ(s):
                            if child in close_list:
                                close_list.remove(child)
                                open_list.append(child)
                else:
                    # 对结点n进行扩展,搜索图添加s结点
                    self.G[s] = Node(s, self.G[n].cost + 1, self.G[n], f = self.G[n].cost+1+h(s))
                    # print(s)# debug
                    cnt_of_gen += 1
                    if s == self.target:
                        return True, cnt_of_gen, cnt_of_expanded + 1
                    open_list.append(s)
                    expanded = True
            open_list = sorted(open_list, key = lambda x : -self.G[x].f)# 按评价函数f从大到小排序
            if expanded:
                cnt_of_expanded += 1
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

    '''
    启发式搜索的启发函数1
    '''
    def h1(self, n):
        W = 0
        for i in range(9):
            if n[i] == ' ':
                continue
            W += (1 if n[i] != self.target[i] else 0)
        return W

    '''
    启发式搜索的启发函数2
    '''
    def h2(self, n):
        P = 0
        for i in range(9):
            if n[i] == ' ':
                continue
            P += abs(i // 3 - self.target.index(n[i]) // 3)
            P += abs(i % 3 - self.target.index(n[i]) % 3)
        return P

    '''
    启发式搜索的启发函数3
    I:*ACDEFGH
    T:ABCDEFGH
    使[当前点，后继点]组成如下数对
    目标状态的数对：[A,B], [B,C], [C,D], [D,E], [E,F], [F,G], [G,H], [H,A]
    当前状态的数对：[A,C], [C,D], [D,E], [E,F], [F,G], [G,H], [H,*]
    ([*,A] 不考虑，因为不存在*这样的前继)
    其中有2对是当前点相同，后继点不同的：[A,C], [H,*]    因此 2*2=4分;
    再把S乘以3：3*(1+2*2）=15分;
    总得分h=P+3S=2+15=17分
    再通过求所有情况的每一步的总花费f=g+h就可以重新对open表排序来进行选择最优策略了。
    '''
    def h3(self, n):
        S = 0
        check_order = [0, 1, 2, 5, 8, 7, 6, 3, 0]
        for i in range(1, 9):
            cur = n[check_order[i - 1]]# i-1是当前牌子,i是后继牌子
            if cur != ' ':
                nxt = n[check_order[i]]
                if cur == '8':
                    if nxt != '1':
                        S += 2
                elif str(int(cur) + 1 ) != nxt:
                    S += 2
        if n[4] != ' ':
            S += 1
        return self.h2(n) + 3 * S

# 本模块的测试入口函数
if __name__ == "__main__":
    s = Solver('2164 8753', max_depth=30)
    print('启发式搜索:')
    flag, cnt_of_gen, cnt_of_expanded = s.hs3()
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



    

 