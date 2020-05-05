import numpy as np
from random import randrange
import random
g_dict_layouts = {}
g_dict_layouts_deep = {} # 搜索深度（所需步数）
g_dict_layouts_fn = {} #当前状态与其fn值的键值对

#每个位置上下左右移动的位置集合
g_dict_shifts = {0:[1, 3], 1:[0, 2, 4], 2:[1, 5],
                 3:[0,4,6], 4:[1,3,5,7], 5:[2,4,8],
                 6:[3,7],  7:[4,6,8], 8:[5,7]}

def swap_chr(a, i, j, deep, destLayout):
    if i > j:
        i, j = j, i
    #得到ij交换后的数组
    b = a[:i] + a[j] + a[i+1:j] + a[i] + a[j+1:]
    #fn = get_wn(b, destLayout)+deep # 存储fn
    fn = get_pn(b, destLayout)+deep # pn
    # fn = 3*get_sn(b, destLayout)+get_pn(b, destLayout)+deep # pn+3sn
    return b, fn

def get_input(num):
    A=[]
    for i in range(9):
        A.append(num[i])
    b=np.array(A).reshape(3,3)
    return b
def getposnum(arr1,num):#获取某数字位置的横纵坐标 x,y
    for i in range(3):
        for j in range(3):
            if num==arr1[i][j]:
                return i,j
def get_wn(src,dest):
    arr1=get_input(src)
    arr2=get_input(dest)
    wn=0
    for i in range(3):
        for j in range(3):
            if(arr1[i][j]!=arr2[i][j] and arr1[i][j]!='0'):
                wn+=1
    return wn
def get_pn(src,dest):#获取绝对距离，p(n)
    arr1=get_input(src)
    arr2=get_input(dest)
    p_num=0
    for i in range(3):
        for j in range(3):
            if arr1[i][j] != arr2[i][j] and arr2[i][j] != '0':
                # print('cal')
                k, m = getposnum(arr1, arr2[i][j])
                d = abs(i - k) + abs(j - m)
                p_num += d
    return p_num
def get_sn(src): #s(n)
    """
    S(n)是对节点n中将牌排列顺序的计分值
    规定对非中心位置的将牌, 顺某一方向检查,
    若某一将牌后面跟的后继者和目标状态相应将牌的顺序相比
    不一致则该将牌估分取2 一致时则估分取0
    对中心位置有将牌时估分取1,无将牌时估分值取0
    所有非中心位置每个将牌估分总和加上中心位置的估分值为S(n)
    """
    arr1=get_input(src)
    sn_num = 0
    if(arr1[1,1] == '0'):#中心位置将牌
        sn_num = 1
    else:
        sn_num = 0
    for y in range(3):   #第一行
        if(int(arr1[0][y]) != y + 1):
            sn_num += 2
    for x in range(1,3):   #第三列
        if(int(arr1[x][2]) != 3 + x):
            sn_num += 2
    if(int(arr1[2][0]) != 7):
        sn_num += 2        
    if(int(arr1[2][1]) != 6):
        sn_num += 2
    if(int(arr1[1][0]) != 8):
        sn_num += 2 
    return sn_num

def solvePuzzle_A(srcLayout, destLayout):
    #先判断srcLayout和destLayout逆序值是否同是奇数或偶数
    # 判断起始状态是否能够到达目标状态，同奇同偶时才是可达
    src=0;dest=0
    for i in range(1,9):
        fist=0
        for j in range(0,i):
          if srcLayout[j]>srcLayout[i] and srcLayout[i]!='0':#0是false,'0'才是数字
              fist=fist+1
        src=src+fist

    for i in range(1,9):
        fist=0
        for j in range(0,i):
          if destLayout[j]>destLayout[i] and destLayout[i]!='0':
              fist=fist+1
        dest=dest+fist
    if (src%2)!=(dest%2):#一个奇数一个偶数，不可达
        return -1, None
       
    g_dict_layouts[srcLayout] = -1  #初始化字典
    g_dict_layouts_deep[srcLayout]= 1 # 搜索深度（所需步数）当前为1
    g_dict_layouts_fn[srcLayout] = 1 + get_pn(srcLayout, destLayout) # fn=d(n)+h(n)此处dn=1
    openlist = []
    openlist.append(srcLayout)#当前状态存入列表
    nodes_expand = nodes_number = 0
    while len(openlist) > 0:
        curLayout = min(g_dict_layouts_fn, key=g_dict_layouts_fn.get)# 选择当前fn值最小的设为current
        # print('curLayout',curLayout)
        del g_dict_layouts_fn[curLayout] 
        openlist.remove(curLayout)#找到最小fn，并移除
        nodes_expand = nodes_expand + 1
        # print("curLayout ",curLayout)
        if curLayout == destLayout:#判断当前状态是否为目标状态
            break
      
        ind_slide = curLayout.index("0")  # 空出的那个位置的索引
        lst_shifts = g_dict_shifts[ind_slide]#当前可移动的位置集合
        for nShift in lst_shifts:
            newLayout, fn = swap_chr(curLayout, nShift, ind_slide, g_dict_layouts_deep[curLayout] + 1, destLayout)
             # print("newLayout",newLayout) 当前结点curLayout生成的子节点，然后循环选择最小的fn加入下一轮
            if g_dict_layouts.get(newLayout) == None:#判断交换后的状态是否已拓展过
                g_dict_layouts_deep[newLayout] = g_dict_layouts_deep[curLayout] + 1#存入当前拓展深度
                g_dict_layouts_fn[newLayout] = fn # 存入当前拓展结点对应的fn键值对
                g_dict_layouts[newLayout] = curLayout # 上一个结点的值
                openlist.append(newLayout)#存入集合
                # print("openlist拓展:",openlist,"对应fn为:",g_dict_layouts_fn)
                nodes_number = nodes_number + 1
    # print('g_dict_layouts_deep搜索树:',g_dict_layouts_deep)
    # print('g_dict_layouts',g_dict_layouts)
    # print('拓展结点数:',g_dict_layouts_deep['123804765'])
    # print('生成结点数:',len(g_dict_layouts_deep)-1)

    lst_steps = []
    lst_steps.append(curLayout)
    while g_dict_layouts[curLayout] != -1:#存入路径
        curLayout = g_dict_layouts[curLayout]
        lst_steps.append(curLayout)
    lst_steps.reverse()
    return 0, lst_steps, nodes_expand, nodes_number, g_dict_layouts_deep[newLayout]

if __name__ == "__main__":
	
    srcLayout = ""
    destLayout = "123804765"
    
    while(1):
        choice=eval(input("请输入你的操作，1为自动生成,2为手动输入"))
        if choice!=1 and choice!=2:
            print("输入错误","\n")
        else:
            break
    if(choice==1):
        ran=random.sample(range(0,9),9)#随机生成初始状态
        for i in ran:
            srcLayout+=str(i)
        #print(srcLayout)
    else:
        print("请输入初始状态如283164705")
        srcLayout = input()
        print(type(srcLayout))

    retCode, lst_steps, nodes_expand, nodes_number, deep = solvePuzzle_A(srcLayout, destLayout)
    
    if retCode != 0:
        print("目标不可达")
    else:
        for nIndex in range(len(lst_steps)):
            print("step #" + str(nIndex + 1))
            print(get_input(lst_steps[nIndex]))
            # print(lst_steps[nIndex][:3])
            # print(lst_steps[nIndex][3:6])
            # print(lst_steps[nIndex][6:])
    # print("搜索深度:"+str(deep))
    print("初始状态:\n",get_input(srcLayout))
    print("目标状态:\n",get_input(destLayout))
    print("拓展节点数:"+str(nodes_expand-1))
    print("生成节点数:"+str(nodes_number))
    
    