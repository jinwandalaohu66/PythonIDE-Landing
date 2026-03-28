import ui
import random
import traceback

class GuessNumberView(ui.View):
    def __init__(self):
        super().__init__()
        
        # 基础视图设置
        self.name = '猜数字游戏'
        self.background_color = '#F2F2F7'
        
        # 游戏配置常量
        self.LOWER_LIMIT = 1
        self.UPPER_LIMIT = 100
        
        # 声明状态变量
        self.target_number = 0
        self.attempts = 0
        self.current_min = 0
        self.current_max = 0
        
        self.setup_ui()
        # 仅初始化逻辑状态，避免在 __init__ 中调起键盘导致崩溃
        self._init_game_state() 
        
    def setup_ui(self):
        content_width = 280
        
        self.title_label = ui.Label(
            text='猜数字',
            font=('<system-bold>', 36),
            alignment=ui.ALIGN_CENTER,
            flex='LR'
        )
        self.title_label.width, self.title_label.height = content_width, 50
        
        self.range_label = ui.Label(
            font=('<system-medium>', 18),
            text_color='#007AFF',
            alignment=ui.ALIGN_CENTER,
            flex='LR'
        )
        self.range_label.width, self.range_label.height = content_width, 30
        
        self.input_field = ui.TextField(
            placeholder='输入数字...',
            font=('<system>', 24),
            alignment=ui.ALIGN_CENTER,
            keyboard_type=ui.KEYBOARD_NUMBER_PAD,
            background_color='white',
            corner_radius=12,
            flex='LR'
        )
        self.input_field.width, self.input_field.height = content_width, 50
        
        self.guess_button = ui.Button(
            title='确 认',
            font=('<system-bold>', 20),
            background_color='#007AFF',
            tint_color='white',
            corner_radius=12,
            action=self.check_guess,
            flex='LR'
        )
        self.guess_button.width, self.guess_button.height = content_width, 50
        
        self.feedback_label = ui.Label(
            font=('<system-medium>', 18),
            alignment=ui.ALIGN_CENTER,
            number_of_lines=0,
            flex='LR'
        )
        self.feedback_label.width, self.feedback_label.height = content_width, 80
        
        self.reset_button = ui.Button(
            title='🔄 重新开始',
            font=('<system-bold>', 18),
            tint_color='#FF3B30',
            action=self.reset_game,
            flex='LR'
        )
        self.reset_button.width, self.reset_button.height = content_width, 50
        
        for subview in [self.title_label, self.range_label, self.input_field, 
                        self.guess_button, self.feedback_label, self.reset_button]:
            self.add_subview(subview)

    def layout(self):
        """覆盖底层布局方法，确保设备旋转时自动完美居中"""
        center_x = self.width / 2
        self.title_label.center = (center_x, 100)
        self.range_label.center = (center_x, 150)
        self.input_field.center = (center_x, 220)
        self.guess_button.center = (center_x, 290)
        self.feedback_label.center = (center_x, 380)
        self.reset_button.center = (center_x, 480)

    def update_range_label(self):
        self.range_label.text = f'目标范围: {self.current_min} - {self.current_max}'

    def show_feedback(self, text, color):
        self.feedback_label.text = text
        self.feedback_label.text_color = color

    def _init_game_state(self):
        """防御性初始化：只管理数据，不涉及任何阻塞式的 UI 动作"""
        self.target_number = random.randint(self.LOWER_LIMIT, self.UPPER_LIMIT)
        self.attempts = 0
        self.current_min = self.LOWER_LIMIT
        self.current_max = self.UPPER_LIMIT
        
        self.update_range_label()
        self.show_feedback('游戏已准备好，请输入数字', '#8E8E93')
        
        self.guess_button.enabled = True
        self.input_field.enabled = True
        self.reset_button.hidden = True
        self.input_field.text = ''

    def check_guess(self, sender):
        """事件回调函数，利用异常捕获构筑防护网"""
        try:
            input_text = self.input_field.text.strip()
            
            # 基础输入校验
            if not input_text:
                self.show_feedback('请输入数字！', '#FF3B30')
                return
                
            if not input_text.isdigit():
                self.show_feedback('请输入有效的整数！', '#FF3B30')
                self.input_field.text = ''
                return
                
            guess = int(input_text)
                
            # 范围越界校验
            if guess < self.LOWER_LIMIT or guess > self.UPPER_LIMIT:
                self.show_feedback(f'超出范围！请输入 {self.LOWER_LIMIT}-{self.UPPER_LIMIT}', '#FF3B30')
                self.input_field.text = ''
                return
                
            self.attempts += 1
            
            # 核心算法：区间单向收窄 
            if guess < self.target_number:
                self.current_min = max(self.current_min, guess + 1)
                self.show_feedback(f'太小了！(已猜 {self.attempts} 次)', '#FF9500')
                self.update_range_label()
                self.input_field.text = ''
                # 延迟调用 begin_editing，避免可能的UI冲突
                ui.delay(0.1, lambda: self.input_field.begin_editing())
                
            elif guess > self.target_number:
                self.current_max = min(self.current_max, guess - 1)
                self.show_feedback(f'太大了！(已猜 {self.attempts} 次)', '#FF9500')
                self.update_range_label()
                self.input_field.text = ''
                # 延迟调用 begin_editing，避免可能的UI冲突
                ui.delay(0.1, lambda: self.input_field.begin_editing())
                
            else:
                # 猜中时的特殊处理
                self.show_feedback(f'🎉 恭喜猜中！答案是 {self.target_number}\n总共猜了 {self.attempts} 次。', '#34C759')
                self.range_label.text = f'正确答案: {self.target_number}'
                
                # 锁定交互并释放键盘
                self.guess_button.enabled = False
                self.input_field.enabled = False
                self.reset_button.hidden = False
                # 延迟调用 end_editing，避免可能的UI冲突
                ui.delay(0.1, lambda: self.input_field.end_editing())
            
        except Exception as e:
            # 简化异常处理，避免显示技术性错误信息
            self.show_feedback('输入有误，请重试', '#FF3B30')
            self.input_field.text = ''
        
    def reset_game(self, sender):
        self._init_game_state()
        # 延迟调用 begin_editing，避免可能的UI冲突
        ui.delay(0.1, lambda: self.input_field.begin_editing())

if __name__ == '__main__':
    view = GuessNumberView()
    view.present('fullscreen')
