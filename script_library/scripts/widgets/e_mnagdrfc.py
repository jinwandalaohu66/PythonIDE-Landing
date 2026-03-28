# -*- coding: utf-8 -*-
"""
电费剩余金额桌面小组件
使用方法：运行脚本生成小组件配置
"""

from widget import Widget, family,SMALL, MEDIUM, LARGE
import datetime
import requests

# ═══════════════════════════════════════════════════════════
# 可修改的配置变量

YHDABH = "自行填入" #抓包修改这里，yhdabh=2MqPtcetcUPDScD==类似这样的
# ═══════════════════════════════════════════════════════════
API_URL = "https://mdej.impc.com.cn/hlwyy/business-jffw/znjf/queryDfInfoNew_new"

PARAMS = {
    "get": "",
    "yhdabh": YHDABH
}
REQUEST_TIMEOUT = 10  # 请求超时时间（秒）

# ═══════════════════════════════════════════════════════════
# 网络请求获取数据
# ═══════════════════════════════════════════════════════════
def fetch_electricity_data():
    """
    从网络获取电费数据
    返回: dict 或 None（请求失败时返回None）
    """
    try:
        response = requests.get(
            API_URL,
            params=PARAMS,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
                "Accept": "application/json"
            }
        )
        response.raise_for_status()
        json_data = response.json()
        
        if json_data.get("code") == 0 and json_data.get("data"):
            return json_data["data"]
        else:
            print(f"API返回异常: code={json_data.get('code')}, msg={json_data.get('msg', '无')}")
            return None
            
    except requests.exceptions.Timeout:
        print("请求超时，请检查网络连接")
        return None
    except requests.exceptions.ConnectionError:
        print("网络连接失败，请检查网络")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
        return None
    except ValueError:
        print("JSON解析失败")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None

# 获取数据
api_data = fetch_electricity_data()

# 如果网络请求失败，使用默认数据
if api_data is None:
    api_data = {
        "gsbh": "--",
        "limitFlag": "--",
        "qjwyj": "0.0",
        "syje": "0.0",
        "name": "网络异常",
        "addr": "--",
        "khxzmc": "--",
        "sfyxjf": "--"
    }

# 提取数据
syje = float(api_data.get("syje", "0"))
name = api_data.get("name", "--")
khxzmc = api_data.get("khxzmc", "--")
now = datetime.datetime.now()

# 判断余额状态
if syje < 10:
    status_color = ("#EF4444", "#F87171")  # 红色 - 余额不足
    status_text = "余额不足"
    status_icon = "exclamationmark.triangle.fill"
elif syje < 50:
    status_color = ("#F59E0B", "#FBBF24")  # 橙色 - 偏低
    status_text = "余额偏低"
    status_icon = "exclamationmark.circle.fill"
else:
    status_color = ("#10B981", "#34D399")  # 绿色 - 正常
    status_text = "余额充足"
    status_icon = "checkmark.circle.fill"

# 创建小组件
w = Widget(background=("#F8FAFC", "#0F172A"), padding=14)

if family == SMALL:
    # 小尺寸：居中显示核心金额
    with w.vstack(spacing=0, align="center"):
        w.spacer()
        w.icon(status_icon, size=16, color=status_color)
        w.spacer(4)
        w.text(f"¥{syje:.1f}", size=26, weight="bold", design="rounded",
               color=("#0F172A", "#F8FAFC"))
        w.spacer(2)
        w.text("电费余额", size=11, color=("#94A3B8", "#64748B"))
        w.spacer()

elif family == MEDIUM:
    # 中尺寸：左侧金额 + 右侧状态信息
    with w.hstack(spacing=0):
        # 左侧：金额显示
        with w.vstack(spacing=4, align="leading"):
            w.icon("bolt.fill", size=14, color="#3B82F6")
            w.text("电费余额", size=12, color=("#94A3B8", "#64748B"))
            w.text(f"¥{syje:.1f}", size=28, weight="bold", design="rounded",
                   color=("#0F172A", "#F8FAFC"))
        w.spacer()
        # 右侧：状态卡片
        with w.card(background=("#F1F5F9", "#1E293B"),
                    corner_radius=10, padding=10, spacing=4):
            w.icon(status_icon, size=16, color=status_color)
            w.text(status_text, size=12, weight="medium",
                   color=("#334155", "#E2E8F0"))
            w.text(f"更新 {now.strftime('%H:%M')}", size=10,
                   color=("#94A3B8", "#64748B"))

else:
    # 大尺寸：完整信息展示
    # 头部
    with w.hstack(spacing=6):
        w.icon("bolt.fill", size=16, color="#3B82F6")
        w.text("电费余额查询", size=16, weight="semibold",
               color=("#334155", "#E2E8F0"))
        w.spacer()
        w.text(f"{now.month}月{now.day}日 {now.strftime('%H:%M')}", size=11,
               color=("#94A3B8", "#64748B"))
    
    w.spacer(10)
    
    # 核心金额卡片
    with w.card(background={"gradient": ["#3B82F6", "#8B5CF6"], "direction": "diagonal"},
                corner_radius=14, padding=16, spacing=4):
        with w.vstack(spacing=4, align="center"):
            w.text("账户余额", size=13, color=("#FFFFFF", "#E0E7FF"), opacity=0.9)
            w.text(f"¥{syje:.1f}", size=36, weight="bold", design="rounded",
                   color=("#FFFFFF", "#FFFFFF"))
            with w.hstack(spacing=4):
                w.icon(status_icon, size=12, color=("#FFFFFF", "#E0E7FF"))
                w.text(status_text, size=12, weight="medium",
                       color=("#FFFFFF", "#E0E7FF"))
    
    w.spacer(10)
    
    # 底部信息卡片
    with w.card(background=("#F1F5F9", "#1E293B"),
                corner_radius=10, padding=12, spacing=0):
        with w.hstack(spacing=0):
            with w.vstack(spacing=2, align="leading"):
                w.text("户主", size=11, color=("#94A3B8", "#64748B"))
                w.text(name, size=13, weight="medium",
                       color=("#334155", "#E2E8F0"))
            w.spacer()
            with w.vstack(spacing=2, align="leading"):
                w.text("用电类型", size=11, color=("#94A3B8", "#64748B"))
                w.text(khxzmc, size=13, weight="medium",
                       color=("#334155", "#E2E8F0"))

w.render()