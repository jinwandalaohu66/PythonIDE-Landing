# keychain 模块 — 完整 API 参考

> Pythonista 兼容安全存储模块，基于 iOS Keychain Services。  
> 用于安全存储 API Key、Token、密码等敏感信息。  
> 数据由 iOS 系统加密，受设备锁保护，跨 App 重装持久化。

---

## 目录

- [快速开始](#快速开始)
- [API 参考](#api-参考)
  - [set_password()](#set_password)
  - [get_password()](#get_password)
  - [delete_password()](#delete_password)
  - [get_services()](#get_services)
- [安全特性](#安全特性)
- [常见用法](#常见用法)
- [与 console 模块配合](#与-console-模块配合)
- [完整示例](#完整示例)

---

## 快速开始

```python
import keychain

# 存储密码
keychain.set_password('github', 'my_account', 'ghp_xxxxxxxxxxxx')

# 读取密码
token = keychain.get_password('github', 'my_account')
print(token)  # ghp_xxxxxxxxxxxx

# 删除密码
keychain.delete_password('github', 'my_account')

# 列出所有存储的凭据
for service, account in keychain.get_services():
    print(f'{service} / {account}')
```

---

## API 参考

### set_password()

```python
keychain.set_password(service, account, password) → bool
```

存储或更新一个密码到 iOS Keychain。如果 `(service, account)` 已存在，则更新。

| 参数 | 类型 | 说明 |
|------|------|------|
| `service` | str | 服务名称（如 `'openai'`、`'github'`） |
| `account` | str | 账户/用户名 |
| `password` | str | 要存储的密码或 token |

**返回值**：`True` 成功，`False` 失败。

```python
keychain.set_password('openai', 'default', 'sk-xxxxxxxx')
keychain.set_password('github', 'user@example.com', 'ghp_xxxxx')
```

### get_password()

```python
keychain.get_password(service, account='') → str or None
```

从 Keychain 读取密码。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `service` | str | 必填 | 服务名称 |
| `account` | str | `''` | 账户名（默认空字符串） |

**返回值**：密码字符串，或 `None`（不存在时）。

```python
token = keychain.get_password('openai', 'default')
if token:
    print('Token 已找到')
else:
    print('未存储 Token')
```

### delete_password()

```python
keychain.delete_password(service, account='') → bool
```

从 Keychain 删除指定条目。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `service` | str | 必填 | 服务名称 |
| `account` | str | `''` | 账户名 |

**返回值**：`True`（成功删除或本来就不存在），`False`（出错）。

```python
keychain.delete_password('github', 'user@example.com')
```

### get_services()

```python
keychain.get_services() → list
```

列出本 App 存储的所有 service/account 对。

**返回值**：`[(service, account), ...]` 元组列表。

```python
for svc, acct in keychain.get_services():
    print(f'服务: {svc}, 账户: {acct}')
```

---

## 安全特性

| 特性 | 说明 |
|------|------|
| **加密存储** | iOS 系统级加密，非明文存储 |
| **设备锁保护** | 设备锁定时数据不可访问（`kSecAttrAccessibleWhenUnlocked`） |
| **跨重装持久** | 卸载重装 App 后数据仍在（标准 Keychain 行为） |
| **App 隔离** | 每个 App 有独立命名空间，其他 App 无法访问 |
| **服务前缀** | 内部使用 `com.pythonide.keychain.` 前缀防止冲突 |

---

## 常见用法

### 存储 API Key

```python
import keychain

keychain.set_password('openai', 'api_key', 'sk-xxxxxxxxxxxxxxxx')
api_key = keychain.get_password('openai', 'api_key')
```

### 存储多个账户

```python
import keychain

keychain.set_password('email', 'work@company.com', 'password1')
keychain.set_password('email', 'personal@gmail.com', 'password2')

pw1 = keychain.get_password('email', 'work@company.com')
pw2 = keychain.get_password('email', 'personal@gmail.com')
```

### 检查并按需设置

```python
import keychain

token = keychain.get_password('github', 'token')
if not token:
    token = input('请输入 GitHub Token: ')
    keychain.set_password('github', 'token', token)
```

---

## 与 console 模块配合

最佳实践：用 `console.input_alert()` 或 `console.password_alert()` 获取用户输入，存入 keychain。

```python
import keychain
import console

def get_api_key(service, account='default'):
    """获取 API Key，不存在则弹窗询问并保存"""
    key = keychain.get_password(service, account)
    if not key:
        try:
            key = console.password_alert(
                f'{service} API Key',
                '请输入你的 API Key（安全存储）'
            )
            keychain.set_password(service, account, key)
            console.hud_alert('已安全保存 🔒')
        except KeyboardInterrupt:
            return None
    return key

# 使用
openai_key = get_api_key('openai')
if openai_key:
    print(f'Key 前缀: {openai_key[:8]}...')
```

---

## 完整示例

### 密码管理器

```python
import keychain
import console

def main():
    console.clear()
    console.set_color(0.3, 0.7, 1.0)
    print('🔐 密码管理器')
    console.set_color()
    print()

    while True:
        try:
            choice = console.alert(
                '密码管理器',
                '选择操作',
                '查看所有', '添加/更新', '删除'
            )
        except KeyboardInterrupt:
            break

        if choice == 1:
            pairs = keychain.get_services()
            if not pairs:
                console.hud_alert('暂无存储的密码')
            else:
                console.set_color(0.2, 0.8, 0.4)
                for svc, acct in pairs:
                    pw = keychain.get_password(svc, acct)
                    masked = pw[:2] + '*' * (len(pw) - 2) if pw and len(pw) > 2 else '***'
                    print(f'  {svc} / {acct}: {masked}')
                console.set_color()

        elif choice == 2:
            try:
                svc = console.input_alert('服务名', '如: github, openai')
                acct = console.input_alert('账户名', '如: user@email.com')
                pw = console.password_alert('密码', '输入密码或 Token')
                if keychain.set_password(svc, acct, pw):
                    console.hud_alert('已安全保存 ✓')
                else:
                    console.hud_alert('保存失败')
            except KeyboardInterrupt:
                pass

        elif choice == 3:
            try:
                svc = console.input_alert('要删除的服务名')
                acct = console.input_alert('要删除的账户名')
                keychain.delete_password(svc, acct)
                console.hud_alert('已删除')
            except KeyboardInterrupt:
                pass

    console.hud_alert('退出密码管理器')

main()
```
