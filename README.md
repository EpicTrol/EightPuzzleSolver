# EightPuzzleSolver
 python3.7使用A*算法采用不同的h(n)实现八数码问题，输出包括拓展结点数和生成结点数。
- 深度优先搜索(depth-first-search)
1.  G:=G0(G0=s), OPEN:=(s), CLOSED:=( ); 
2.  LOOP:    IF OPEN=( ) THEN EXIT (FAIL); 
3.  n:   =LAST(OPEN); 
4.  IF GOAL(n) THEN EXIT (SUCCESS); 
5.  REMOVE(n, OPEN), APPEND(n, CLOSED); 
6.  IF DEPTH(n)≥Dm GO LOOP; 
7.  EXPAND(n) →{mi}, G:   =ADD(mi, G); 
8.  IF 目标在{mi}中 THEN EXIT(SUCCESS); 
9.  APPEND(mj, OPEN), 并标记mj到n的指针; 
10. GO LOOP; 

- 宽度优先搜索(breadth-first-search)
1.  G:=G0(G0=s), OPEN:=(s), CLOSED:=( ); 
2.  LOOP:    IF OPEN=( ) THEN EXIT (FAIL); 
3.  n:   =FIRST(OPEN); 
4.  IF GOAL(n) THEN EXIT (SUCCESS); 
5.  REMOVE(n, OPEN), ADD(n, CLOSED); 
6.  IF DEPTH(n)≥Dm GO LOOP; 
7.  EXPAND(n) →{mi}, G:   =ADD(mi, G); 
8.  IF 目标在{mi}中 THEN EXIT(SUCCESS); 
9.  ADD(mj, OPEN), 并标记mj到n的指针; 
10.  GO LOOP; 

+ 启发式搜索算法
  （h1(n) =W(n) “不在位”的将牌数）
  （h2(n) = P(n)将牌“不在位”的距离和）
  （h3(n) = h(n)＝P(n)+3S(n)） 

+ 更换不同的h(n)：
  第18行`swap_chr`中的
  
    ```
    fn = get_wn(b, destLayout)+deep
    ```
  第106行`solvePuzzle_A()`中的
    ```
    g_dict_layouts_fn[srcLayout] = 1 + get_wn(srcLayout, destLayout)
    ```
- 随机产生或手动输入初始状态，对于同一个初始状态，分别用上面的5种方法进行求解，并对比结果

| 方法      | 深度优先 | 宽度优先 | h_1(n) | h2(n) | h3(n) |
| -------------- | ------------ | ------------ | ------ | ----------------- | ----------------- |
| 扩展结点数 |              |              |        |                   |                   |
| 生成结点数 |              |              |        |                   |                   |

gui原型图

![image-20200509234305486](README/image-20200509234305486.png)

运行命令:切换从puzzle文件夹,命令行输入`python gui.py`