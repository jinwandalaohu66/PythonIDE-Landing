# console 模块 — 完整 API 参考

> Pythonista 兼容控制台交互模块。  
> 提供原生 UIAlertController 弹窗、HUD 提示、控制台文本样式和清屏功能。  
> 所有弹窗阻塞调用线程直到用户响应，匹配 Pythonista 的同步 API 行为。

---

## 目录

- [快速开始](#快速开始)
- [弹窗函数](#弹窗函数)
  - [alert()](#alert)
  - [input_alert()](#input_alert)
  - [login_alert()](#login_alert)
  - [password_alert()](#password_alert)
  - [hud_alert()](#hud_alert)
- [控制台格式](#控制台格式)
  - [set_color()](#set_color)
  - [set_font()](#set_font)
  - [clear()](#clear)
  - [write_link()](#write_link)
- [与其他模块组合使用](#与其他模块组合使用)
- [完整示例](#完整示例)

---

## 快速开始

```python
import console

# 弹出原生确认框
choice = console.alert('确认', '是否继续?', '继续', '取消')

# 输入文本
name = console.input_alert('姓名', '请输入你的名字')

# HUD 提示
console.hud_alert('操作成功 ✓')

# 彩色输出
console.set_color(1.0, 0.0, 0.0)  # 红色
print('这是红色文字')
console.set_color()  # 重置
```

---

## 弹窗函数

所有弹窗使用原生 `UIAlertController` 实现，阻塞当前线程直到用户响应。  
用户点击 Cancel 时抛出 `KeyboardInterrupt`。

### alert()

```python
console.alert(title, message='', button1='OK', button2='', button3='',
              hide_cancel_button=False)
```

显示模态弹窗，最多 3 个自定义按钮 + Cancel。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `title` | str | 必填 | 弹窗标题 |
| `message` | str | `''` | 弹窗消息体 |
| `button1` | str | `'OK'` | 第 1 个按钮标题 |
| `button2` | str | `''` | 第 2 个按钮标题（空则不显示） |
| `button3` | str | `''` | 第 3 个按钮标题（空则不显示） |
| `hide_cancel_button` | bool | `False` | 是否隐藏 Cancel 按钮 |

**返回值**：按钮索引（1-based）。Cancel 抛出 `KeyboardInterrupt`。

```python
try:
    idx = console.alert('删除文件?', '此操作不可恢复', '删除', '保留')
    if idx == 1:
        print('用户选择删除')
    elif idx == 2:
        print('用户选择保留')
except KeyboardInterrupt:
    print('用户取消')
```

### input_alert()

```python
console.input_alert(title, message='', input_text='',
                    ok_button_title='OK', hide_cancel_button=False)
```

带文本输入框的弹窗。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `title` | str | 必填 | 标题 |
| `message` | str | `''` | 消息 |
| `input_text` | str | `''` | 输入框默认文本 |
| `ok_button_title` | str | `'OK'` | 确认按钮标题 |
| `hide_cancel_button` | bool | `False` | 是否隐藏 Cancel |

**返回值**：用户输入的文本（str）。Cancel 抛出 `KeyboardInterrupt`。

```python
try:
    name = console.input_alert('姓名', '请输入你的名字', '张三')
    print(f'你好, {name}!')
except KeyboardInterrupt:
    print('已取消')
```

### login_alert()

```python
console.login_alert(title, message='', login='', password='',
                    ok_button_title='OK')
```

登录弹窗，含用户名和密码两个输入框（密码框为安全文本）。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `title` | str | 必填 | 标题 |
| `message` | str | `''` | 消息 |
| `login` | str | `''` | 用户名默认值 |
| `password` | str | `''` | 密码默认值 |
| `ok_button_title` | str | `'OK'` | 确认按钮标题 |

**返回值**：`(username, password)` 元组。Cancel 抛出 `KeyboardInterrupt`。

```python
try:
    user, pw = console.login_alert('登录', '请输入服务器凭据')
    print(f'用户: {user}')
except KeyboardInterrupt:
    print('已取消登录')
```

### password_alert()

```python
console.password_alert(title, message='', password='',
                       ok_button_title='OK')
```

密码输入弹窗（安全文本框，内容不可见）。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `title` | str | 必填 | 标题 |
| `message` | str | `''` | 消息 |
| `password` | str | `''` | 默认密码 |
| `ok_button_title` | str | `'OK'` | 确认按钮标题 |

**返回值**：用户输入的密码（str）。Cancel 抛出 `KeyboardInterrupt`。

```python
try:
    pw = console.password_alert('授权', '请输入管理员密码')
except KeyboardInterrupt:
    print('已取消')
```

### hud_alert()

```python
console.hud_alert(message, icon='', duration=1.5)
```

显示一个短暂的 HUD 覆盖提示，自动消失。不阻塞。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `message` | str | 必填 | 提示文本 |
| `icon` | str | `''` | 可选 emoji 或图标 |
| `duration` | float | `1.5` | 显示时长（秒） |

```python
console.hud_alert('已保存 ✓', duration=2.0)
console.hud_alert('下载完成', icon='📦')
```

---

## 控制台格式

### set_color()

```python
console.set_color(r, g, b)    # 设置颜色
console.set_color()            # 重置为默认颜色
```

设置后续 `print()` 输出的文本颜色。

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| `r` | float | 0.0–1.0 | 红色分量 |
| `g` | float | 0.0–1.0 | 绿色分量 |
| `b` | float | 0.0–1.0 | 蓝色分量 |

无参数调用时重置为默认颜色。

```python
console.set_color(1, 0, 0)   # 红色
print('错误信息')
console.set_color(0, 0.8, 0)  # 绿色
print('成功信息')
console.set_color()            # 重置
```

### set_font()

```python
console.set_font(name, size)   # 设置字体
console.set_font()              # 重置
```

设置控制台字体。iOS 上主要影响文字粗细（size > 16 显示粗体）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | str | 字体名称（信息性） |
| `size` | float | 字号；> 16 使用粗体 |

### clear()

```python
console.clear()
```

清空控制台输出。

### write_link()

```python
console.write_link(title, url='', font=None)
```

在控制台输出一个可点击的超链接。

| 参数 | 类型 | 说明 |
|------|------|------|
| `title` | str | 链接显示文本 |
| `url` | str | 目标 URL |
| `font` | tuple | 可选 `(font_name, size)` 元组 |

```python
console.write_link('打开 GitHub', 'https://github.com')
```

---

## 与其他模块组合使用

### console + keychain（安全存储 API Key）

```python
import console
import keychain

api_key = keychain.get_password('openai', 'api_key')
if not api_key:
    api_key = console.input_alert('API Key', '请输入 OpenAI API Key')
    keychain.set_password('openai', 'api_key', api_key)

console.hud_alert('API Key 已就绪 ✓')
```

### console + sound（游戏提示）

```python
import console
import sound

try:
    name = console.input_alert('玩家', '输入你的名字')
    sound.play_effect('ui:click1')
    console.hud_alert(f'欢迎, {name}!')
except KeyboardInterrupt:
    pass
```

---

## 完整示例

### 交互式笔记本

```python
import console

console.clear()
console.set_color(0.2, 0.6, 1.0)
print('=== 我的笔记本 ===')
console.set_color()

notes = []

while True:
    try:
        choice = console.alert('操作', '', '添加笔记', '查看全部', '清空')
    except KeyboardInterrupt:
        break

    if choice == 1:
        try:
            note = console.input_alert('新笔记', '输入内容')
            notes.append(note)
            console.hud_alert(f'已添加（共 {len(notes)} 条）')
        except KeyboardInterrupt:
            pass
    elif choice == 2:
        if notes:
            for i, n in enumerate(notes, 1):
                console.set_color(0.8, 0.8, 0.2)
                print(f'{i}. {n}')
            console.set_color()
        else:
            console.hud_alert('暂无笔记')
    elif choice == 3:
        notes.clear()
        console.clear()
        console.hud_alert('已清空')

console.hud_alert('退出笔记本')
```
