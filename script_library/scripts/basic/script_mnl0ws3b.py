import math
import sys

class ScientificCalculator:
    def __init__(self):
        self.memory = 0
        self.history = []
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
            'inf': float('inf'),
            'nan': float('nan')
        }
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'log': math.log10,
            'ln': math.log,
            'log2': math.log2,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'cbrt': lambda x: x ** (1/3),
            'abs': abs,
            'floor': math.floor,
            'ceil': math.ceil,
            'round': round,
            'fact': math.factorial,
            'gamma': math.gamma,
            'erf': math.erf
        }
    
    def evaluate(self, expression):
        """计算表达式"""
        try:
            # 替换常量
            for name, value in self.constants.items():
                expression = expression.replace(name, str(value))
            
            # 安全评估
            allowed_names = {k: v for k, v in self.functions.items()}
            allowed_names.update({
                'pi': math.pi,
                'e': math.e,
                'tau': math.tau,
                'inf': float('inf'),
                'nan': float('nan')
            })
            allowed_names.update({name: getattr(math, name) for name in dir(math) 
                                  if not name.startswith('_')})
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            # 保存到历史
            self.history.append((expression, result))
            if len(self.history) > 50:
                self.history.pop(0)
            
            return result
        except Exception as e:
            return f"错误: {str(e)}"
    
    def show_menu(self):
        print("\n" + "=" * 60)
        print("             科学计算器 Scientific Calculator")
        print("=" * 60)
        print("支持运算: +, -, *, /, **, //, %")
        print("数学函数: sin, cos, tan, asin, acos, atan")
        print("          sinh, cosh, tanh, log, ln, log2")
        print("          sqrt, cbrt, exp, abs, floor, ceil")
        print("          fact(阶乘), gamma, erf")
        print("常量: pi, e, tau")
        print("=" * 60)
        print("特殊命令:")
        print("  m+          - 存入内存")
        print("  m-          - 从内存减去")
        print("  mr          - 读取内存")
        print("  mc          - 清空内存")
        print("  history     - 查看历史")
        print("  clear/h     - 清屏")
        print("  constants   - 查看常量")
        print("  help/?      - 显示帮助")
        print("  q/exit      - 退出")
        print("=" * 60)
    
    def show_constants(self):
        print("\n当前常量:")
        for name, value in self.constants.items():
            print(f"  {name} = {value}")
    
    def run(self):
        print("\n科学计算器已启动")
        print("输入 'help' 查看帮助")
        
        while True:
            try:
                # 获取输入
                user_input = input("\n>>> ").strip().lower()
                
                if not user_input:
                    continue
                
                # 处理命令
                if user_input in ['q', 'exit', 'quit']:
                    print("再见！")
                    break
                
                elif user_input in ['help', '?']:
                    self.show_menu()
                
                elif user_input in ['clear', 'h', 'cls']:
                    import os
                    os.system('clear' if os.name == 'posix' else 'cls')
                
                elif user_input == 'history':
                    if not self.history:
                        print("暂无历史记录")
                    else:
                        print("\n历史记录:")
                        for i, (expr, result) in enumerate(self.history[-10:], 1):
                            print(f"  {i}. {expr} = {result}")
                
                elif user_input == 'constants':
                    self.show_constants()
                
                elif user_input == 'm+':
                    try:
                        expr = input("输入要存入内存的表达式: ")
                        result = self.evaluate(expr)
                        if isinstance(result, (int, float)):
                            self.memory += result
                            print(f"内存 += {result} = {self.memory}")
                        else:
                            print(result)
                    except:
                        print("无效表达式")
                
                elif user_input == 'm-':
                    try:
                        expr = input("输入要从内存减去的表达式: ")
                        result = self.evaluate(expr)
                        if isinstance(result, (int, float)):
                            self.memory -= result
                            print(f"内存 -= {result} = {self.memory}")
                        else:
                            print(result)
                    except:
                        print("无效表达式")
                
                elif user_input == 'mr':
                    print(f"内存值: {self.memory}")
                
                elif user_input == 'mc':
                    self.memory = 0
                    print("内存已清空")
                
                else:
                    # 计算表达式
                    result = self.evaluate(user_input)
                    if isinstance(result, (int, float)):
                        # 格式化输出
                        if isinstance(result, float) and result.is_integer():
                            result = int(result)
                        print(f"= {result}")
                    else:
                        print(result)
            
            except KeyboardInterrupt:
                print("\n使用 'q' 退出")
            except Exception as e:
                print(f"错误: {e}")


def main():
    calc = ScientificCalculator()
    calc.run()


if __name__ == "__main__":
    main()