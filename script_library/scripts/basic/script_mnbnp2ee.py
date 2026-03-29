def Menu(): #定义界面
    print(('-' * 20))
    print('简易数学计算器系统1.0')
    print('1.加法运算 2.减法运算 3.乘法运算')
    print('4.除法运算 0.退出系统')
    print(('-' * 20))

def jia(): #定义加法函数
    a = float(input('请输入加数1：'))
    b = float(input('请输入加数2：'))
    c = a + b
    print('和为：',c)

def jian(): #定义减法函数
    d = float(input('请输入被减数：'))
    e = float(input('请输入减数：'))
    f = d - e
    print('差为：',f)

def cheng(): #定义乘法函数
    g = float(input('请输入乘数1：'))
    h = float(input('请输入乘数2：'))
    i = g * h
    print('积为：',i)

def chu(): #定义除法函数
    j = float(input('请输入被除数：'))
    k = float(input('请输入除数：'))
    l = j / k
    print('商为：',l)

def main(): #定义主控制台
    while True:
        Menu()
        key = input('请输入对应功能的数字：')
        if key == '1':
            jia()
        elif key == '2' :
            jian()
        elif key == '3' :
            cheng()
        elif key == '4' :
            chu()
        elif key == '0' :
            q = input('是否退出系统？（y or n)：')
            if q == 'y':
                print('已退出系统')
                break
        else :
            print('没有对应此数字的功能！')

main() #调用主函数

    
