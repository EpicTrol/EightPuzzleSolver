# encoding: utf-8
'''
Created on 2020年05月09日
@author: Liang Zehao
@file: solver.py
@description: 八数码搜索算法
'''

class Node:
    def __init__(self, data, cost = 0, parent = None):
        self.data = data
        self.parent = parent
        self.cost = cost
        self.level = cost

class Solver:
    def __init__(self, max_depth = 20):
        self.target = '1234 5678'
        self.max_depth = max_depth

    '''
    :param n 状态n
    :yield 迭代器返回一个后继状态
    '''
    def succ(self, n):
        arr = [char for char in n]
        idx = arr.index(' ')# 空格的索引位置
        # 右移空格
        if idx not in [2, 5, 8]:
            arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]
            yield ''.join(arr)
        # 左移空格
        if idx not in [0, 3, 6]:
            arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]
            yield ''.join(arr)
        # 上移空格
        if idx > 2:
            arr[idx], arr[idx - 3] = arr[idx - 3], arr[idx]
            yield ''.join(arr)
        # 下移空格
        if idx < 6:
            arr[idx], arr[idx + 3] = arr[idx + 3], arr[idx]
            yield ''.join(arr)

    '''
    :param s0 初始状态,格式如:'1234567 8'
    :return 返回的第一个值是是否找到解路，返回的第二个值是生成的节点数, 第三个值是被扩展的节点数
    '''
    def dfs(self, s0):
        cnt_of_gen = 0# 生成的节点数
        cnt_of_expanded = 0# 被扩展的节点数
        open_list = [s0]
        close_list = []
        G = {s0:Node(s0)}# 搜索图
        while open_list:
            n = open_list.pop()
            # 找到解
            if n == self.target:
                return True, cnt_of_gen, cnt_of_expanded
            close_list.append(n)
            # 搜索深度超过限制
            if G[n].level >= self.max_depth:
                continue
            expanded = False
            # 遍历后继状态
            for s in self.succ(n):
                # 如果后继结点已经出现过,则考虑修改cost和父指针,不新建结点
                if s in G:
                    if G[n].cost + 1 < G[s].cost:
                        G[s].cost = G[n].cost + 1
                        G[s].parent = G[n]
                else:
                    # 对结点n进行扩展,搜索图添加s结点
                    G[s] = Node(s, G[n].cost + 1, G[n])
                    cnt_of_gen += 1
                    if s == self.target:
                        return True, cnt_of_gen, cnt_of_expanded + 1
                    open_list.append(s)
                    expanded = True
            if expanded:
                cnt_of_expanded += 1
        return False, cnt_of_gen, cnt_of_expanded

if __name__ == "__main__":
    flag, cnt_of_gen, cnt_of_expanded = Solver().dfs('2831647 5')
    print(flag, cnt_of_gen, cnt_of_expanded)
                

 