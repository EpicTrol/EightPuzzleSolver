import random

'''
@param mode 初始状态的产生模式, mode=0随机产生, mode=1手动输入
'''
def genInitState(mode=0):
    if mode == 0:
        return ''.join(random.sample(range(0, 9), 9)).replace('0', ' ')
    else:
        s = [int] * 9
        for i in range(9):
            strin = input('输入初始状态序列,以空格分割')
            arr = strin.split(' ')
            
            return [e for e in arr]

if __name__ == "__main__":
    print(genInitState(1))
        