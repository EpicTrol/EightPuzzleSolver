# EightPuzzleSolver
 python3.7使用A*算法采用不同的h(n)实现八数码问题，输出包括拓展结点数和生成结点数。

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