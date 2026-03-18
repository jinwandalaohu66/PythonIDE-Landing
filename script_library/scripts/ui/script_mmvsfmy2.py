import ui
import re

# 只允许安全的计算表达式
_allowed_pattern = re.compile(r'^[0-9+\-*/().\s]+$')

def safe_eval(expr: str):
    expr = expr.strip()
    if not expr:
        return ''
    if not _allowed_pattern.match(expr):
        return 'Error'
    try:
        result = eval(expr, {"__builtins__": None}, {})
        if isinstance(result, float):
            return str(int(result)) if result.is_integer() else str(result)
        return str(result)
    except Exception:
        return 'Error'


class SimpleCalculator(ui.View):
    def __init__(self, *args, **kwargs):
        # 模拟“正常用户”：给一个典型根尺寸 320x480
        super().__init__(frame=(0, 0, 320, 480), *args, **kwargs)

        self.background_color = 'white'
        self.name = '计算器(测试UI居中)'
        self.expr = '0'

        # 顶部显示区域 —— 占一点高度，不压得太高，也不太低
        self.display = ui.Label()
        self.display.frame = (16, 40, self.width - 32, 60)
        self.display.alignment = ui.ALIGN_RIGHT
        self.display.font = ('<System>', 32)
        self.display.text = '0'
        self.display.text_color = 'black'
        self.display.background_color = None
        self.add_subview(self.display)

        # 按钮布局：整体放在中部偏下，但不是挤到最下面
        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '',   '.', '='],
        ]

        margin = 10
        btn_w = (self.width - margin * 5) / 4.0
        btn_h = 60
        # 比你之前的 140 再往上提一点，整体更居中
        start_y = 120

        for row_index, row in enumerate(buttons):
            for col_index, title in enumerate(row):
                if title == '':
                    continue

                x = margin + col_index * (btn_w + margin)
                y = start_y + row_index * (btn_h + margin)

                # 0 键双倍宽度
                if title == '0' and row_index == 4 and col_index == 0:
                    width = btn_w * 2 + margin
                else:
                    width = btn_w

                btn = ui.Button(title=title)
                btn.frame = (x, y, width, btn_h)
                btn.font = ('<System>', 24)
                btn.corner_radius = 12

                if title in ['C', '+/-', '%']:
                    btn.background_color = '#a5a5a5'
                    btn.tint_color = 'black'
                elif title in ['/', '*', '-', '+', '=']:
                    btn.background_color = '#ff9f0a'
                    btn.tint_color = 'white'
                else:
                    btn.background_color = '#333333'
                    btn.tint_color = 'white'

                btn.action = self.button_tapped
                self.add_subview(btn)

    # 更新显示
    def update_display(self):
        self.display.text = self.expr

    # 按钮事件
    def button_tapped(self, sender):
        text = sender.title

        if text == 'C':
            self.expr = '0'
            self.update_display()
            return

        if text == '+/-':
            if self.expr.startswith('-'):
                self.expr = self.expr[1:]
            else:
                if self.expr != '0':
                    self.expr = '-' + self.expr
            self.update_display()
            return

        if text == '%':
            val = safe_eval(self.expr)
            if val not in ('Error', ''):
                try:
                    num = float(val) / 100.0
                    self.expr = str(int(num)) if num.is_integer() else str(num)
                except Exception:
                    self.expr = 'Error'
            else:
                self.expr = 'Error'
            self.update_display()
            return

        if text == '=':
            result = safe_eval(self.expr)
            self.expr = result if result != '' else '0'
            self.update_display()
            return

        # 普通数字/符号输入
        if self.expr == '0' and text in '0123456789':
            self.expr = text
        else:
            self.expr += text

        self.update_display()


def main():
    v = SimpleCalculator()
    v.present('sheet')


if __name__ == '__main__':
    main()