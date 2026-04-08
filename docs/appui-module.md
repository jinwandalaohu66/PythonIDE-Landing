# appui 模块 — 声明式原生 UI（SwiftUI 风格）

`appui` 是 Python IDE 提供的 **声明式 UI 框架**：用 Python 描述界面结构（栈、列表、表单、导航等），底层由 **SwiftUI** 渲染，适合快速搭建设置页、简单工具界面、原型等场景。

> **与内置帮助一致**：应用内 **设置 → 帮助 → 模块与原生能力指南 → appui — 声明式 UI 框架** 中有与本文同步的速查示例。

---

## 与 `ui` 模块的区别

| 维度 | `ui` 模块 | `appui` 模块 |
|------|-----------|--------------|
| **风格** | Pythonista 兼容的 **UIKit 命令式** API | **声明式** DSL，接近 SwiftUI |
| **典型用法** | `ui.View`、`present()`、`load_view`、手势、自定义 `draw` | `appui.VStack`、`appui.run()`、链式 **修饰符** |
| **状态** | 手动更新控件属性 | `appui.State` **响应式**，改属性可触发界面刷新 |
| **坐标** | 左上角原点，`y` 向下 | 由布局容器与修饰符管理，不写绝对 frame 也能排版 |
| **兼容目标** | 与 Pythonista 脚本、老项目对齐 | 新项目、快速界面、SwiftUI 心智模型 |

两者可同时存在于应用中，按场景选择：**复杂传统 UI / 兼容 Pythonista** 用 `ui`；**列表+表单+导航的现代布局** 可优先尝试 `appui`。

---

## 快速开始

```python
import appui

state = appui.State(count=0)

def increment():
    state.count += 1

def body():
    return appui.VStack([
        appui.Text(f"计数: {state.count}")
            .font("title").bold(),
        appui.Button("点击 +1", action=increment)
            .button_style("bordered_prominent"),
    ], spacing=20).padding()

appui.run(body, state=state)
```

---

## 入口与展示

| API | 说明 |
|-----|------|
| `appui.run(body, state=..., presentation=...)` | 运行声明式界面；`body` 为无参函数，返回根视图 |
| `presentation` | `'sheet'` / `'fullscreen'` / `'fullscreen_with_close'` 等，控制模态样式 |

---

## 布局容器

```python
# 垂直 / 水平 / 层叠
appui.VStack(content, alignment, spacing)
appui.HStack(content, alignment, spacing)
appui.ZStack(content, alignment)

# 滚动与网格
appui.ScrollView(content, axes='vertical')
appui.LazyVGrid(columns=[appui.flexible()], content)

# 列表与表单
appui.List(content)
appui.Form([
    appui.Section(content, header="标题"),
])
appui.ForEach(data, row_builder, key='id')
```

| 组件 | 用途 |
|------|------|
| `VStack` / `HStack` / `ZStack` | 线性或叠加布局 |
| `ScrollView` | 可滚动内容 |
| `LazyVGrid` + `flexible()` | 自适应列网格 |
| `List` | 列表 |
| `Form` / `Section` | 分组表单 |
| `ForEach` | 由数据驱动多行 |

---

## 导航与标签页

```python
# 导航栈
appui.NavigationStack(
    appui.VStack([...])
        .navigation_title("首页")
)
appui.NavigationLink("详情", destination=detail())

# 底部标签页
appui.TabView([
    appui.Tab(title="首页",
        system_image="house.fill",
        content=home_view()),
    appui.Tab(title="设置",
        system_image="gearshape.fill",
        content=settings_view()),
])
```

---

## 基础视图与输入控件

**展示**

- `appui.Text(...)`  
- `appui.Image(system_name="star.fill")` — SF Symbol  

**输入**

```python
appui.TextField("占位符", text=state.name,
    on_change=lambda v: setattr(state, 'name', v))
appui.SecureField("密码", text=state.pwd, ...)
appui.TextEditor(text=state.note, on_change=...)
appui.Toggle("开关", is_on=state.on, on_change=...)
appui.Slider(value=state.val, minimum=0, maximum=100)
appui.Picker("选择", selection=state.sel,
    options=["A", "B", "C"], on_change=...)
appui.DatePicker("日期", selection=state.date)
```

---

## 修饰符（链式调用）

声明式 API 通过 **返回 self** 的链式方法设置样式与行为：

```python
appui.Text("Hello")
    .font("title")
    .bold()
    .foreground_color("blue")
    .padding(16)
    .background("gray", corner_radius=12)
    .frame(width=200, height=100)
    .shadow(radius=4)
    .on_tap(action)
    .animation("spring")

appui.Image(system_name="star.fill")
    .font("system", size=48)
    .resizable()
    .aspect_ratio(content_mode='fit')
    .foreground_color("orange")
```

常见修饰符包括：`font`、`bold`、`foreground_color`、`padding`、`background`、`frame`、`shadow`、`on_tap`、`animation` 等（以实际实现为准）。

---

## 状态管理

```python
# 响应式状态 — 属性变化会驱动 UI 更新
state = appui.State(count=0, name='')
state.count += 1

# 不触发刷新的引用容器
ref = appui.Ref(initial=None)

# 计算属性（依赖变化时重算）
@appui.computed(state, depends_on=['count'])
def doubled():
    return state.count * 2

# 副作用（依赖变化时执行）
@appui.effect(state, depends_on=['name'])
def on_name_change():
    print(f"名字变为: {state.name}")
```

| 类型 | 作用 |
|------|------|
| `State` | 可观察状态，赋值后刷新依赖该状态的视图 |
| `Ref` | 可变引用，适合存放不需要触发整树刷新的对象 |
| `@computed` | 派生数据 |
| `@effect` | 依赖变更时的回调（日志、同步等） |

---

## 手势与弹窗

```python
# 手势
.on_tap(action)
.on_long_press(action, min_duration=0.5)
.on_drag(on_changed=..., on_ended=...)

# 弹窗
.alert("标题", message="内容",
    is_presented=state.show_alert,
    actions=[appui.Button("确定", action=ok)])
.sheet(is_presented=state.show_sheet,
    content=sheet_view())
```

`appui.Button` 既可用在布局中，也可作为 `alert` 的 `actions`。

---

## 完整示例：计数器 + 多状态

```python
import appui

state = appui.State(count=0, show_alert=False)

def increment():
    state.count += 1

def body():
    return appui.NavigationStack(
        appui.VStack([
            appui.Text(f"当前: {state.count}").font("title"),
            appui.Button("+1", action=increment),
            appui.Button("弹出提示", action=lambda: setattr(state, "show_alert", True)),
        ], spacing=16)
        .padding()
        .navigation_title("Demo")
        .alert(
            "提示",
            message="这是一个 alert 示例",
            is_presented=state.show_alert,
            actions=[appui.Button("好的", action=lambda: setattr(state, "show_alert", False))],
        )
    )

appui.run(body, state=state, presentation='sheet')
```

---

## 注意事项

1. **线程**：UI 更新应在主线程/框架允许的上下文中进行（与 `ui` 模块相同，避免后台线程直接改 State）。  
2. **与 `scene` 坐标系无关**：`appui` 为屏幕 UI；2D 游戏请使用 `scene` 模块。  
3. **API 演进**：链式修饰符与控件名可能随版本增加，若 AI 助手或文档滞后，请以 **应用内「模块与原生能力指南」** 为准。

---

## 相关文档

- [ui 模块 — 原生 iOS 界面](ui-module.md)（Pythonista / UIKit）  
- [scene 模块 — 2D 游戏引擎](scene-module.md)  
- [widget 模块 — 桌面小组件](widget-module.md)
