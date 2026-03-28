# 92-95每日油价桌面小组件
# 数据来源：20121212.cn 油价接口
# 城市可自定义设置
# 注意：每次刷新都会从网络获取最新数据，无缓存

from widget import Widget, family, SMALL, MEDIUM, LARGE
import datetime
import json

# ═══════════════════════════════════════════════════════════
# 配置区 - 设置你所在的城市
# 支持城市：北京、上海、广州、深圳、杭州、南京、武汉、成都、重庆、西安、天津 等
# ═══════════════════════════════════════════════════════════
CITY_NAME = "北京"  # ← 在这里修改城市名称

# ═══════════════════════════════════════════════════════════
# 油价API接口
# ═══════════════════════════════════════════════════════════
OIL_PRICE_API = "https://20121212.cn/ci/index.php/iol/like/"


def get_oil_price_from_api(city_name):
    """
    从油价API获取数据
    接口：https://20121212.cn/ci/index.php/iol/like/{城市名}
    """
    try:
        import requests
    except ImportError:
        return None
    
    url = f"{OIL_PRICE_API}{city_name}"
    
    try:
        resp = requests.get(url, timeout=10)
        text = resp.text
        resp.close()
        
        # 解析JSON数据
        data = json.loads(text)
        
        # 检查是否成功返回数据
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            
            return {
                "price92": float(item.get("iol92", 0)),
                "price95": float(item.get("iol95", 0)),
                "price98": float(item.get("iol98", 0)),
                "price89": float(item.get("iol89", 0)),
                "price0": float(item.get("iol0", 0)),
                "price10": float(item.get("iol10", 0)),
                "price20": float(item.get("iol20", 0)),
                "price35": float(item.get("iol35", 0)),
                "ton92": item.get("ton92", ""),
                "ton95": item.get("ton95", ""),
                "ton98": item.get("ton98", ""),
                "update": item.get("date", ""),
                "city_raw": item.get("city", ""),
            }
    except Exception as e:
        print(f"API请求失败: {e}")
    
    return None


def get_oil_price(city_name=None):
    """
    获取油价数据（直接请求API，不使用缓存）
    """
    # 使用配置的城市名
    if not city_name:
        city_name = CITY_NAME
    
    # 直接从API获取
    api_data = get_oil_price_from_api(city_name)
    if api_data:
        return api_data, city_name, True
    
    # API不可用，返回失败状态
    return None, city_name, False


# ═══════════════════════════════════════════════════════════
# 主程序 - 小组件渲染
# ═══════════════════════════════════════════════════════════

# 获取油价数据
oil_data, current_city, data_ok = get_oil_price()
now = datetime.datetime.now()

# 配色方案 - 暖白主题
BG_COLOR = ("#FFFBEB", "#1C1917")
CARD_BG = ("#FEF3C7", "#292524")
TITLE_COLOR = ("#78350F", "#FDE68A")
TEXT_COLOR = ("#92400E", "#D6D3D1")
SUB_COLOR = ("#B45309", "#78716C")
ACCENT_COLOR = ("#EA580C", "#FB923C")
ERROR_COLOR = ("#DC2626", "#F87171")

# 创建小组件
w = Widget(background=BG_COLOR, padding=14)

if family == SMALL:
    # ═══ SMALL (127×127pt) ═══
    # 极简设计：单行展示核心油价，居中显示
    with w.vstack(spacing=0, align="center"):
        w.spacer()  # 顶部弹性
        
        # 图标 + 标题
        w.icon("fuelpump.fill", size=16, color=ACCENT_COLOR)
        w.spacer(4)
        w.text("油价", size=11, weight="medium", color=SUB_COLOR)
        
        w.spacer(6)
        
        # 核心数据
        if data_ok and oil_data:
            price92 = oil_data.get("price92", 0)
            with w.hstack(spacing=8):
                w.text("92#", size=12, weight="semibold", color=TEXT_COLOR)
                w.text(f"¥{price92:.2f}", size=20, weight="bold", 
                       design="rounded", color=TITLE_COLOR)
        else:
            w.text("N/A", size=20, weight="bold", 
                   design="rounded", color=ERROR_COLOR)
        
        w.spacer(4)
        
        # 副标题
        if data_ok:
            w.text(current_city, size=10, color=SUB_COLOR)
        else:
            w.text("网络异常", size=10, color=ERROR_COLOR)
        
        w.spacer()  # 底部弹性

elif family == MEDIUM:
    # ═══ MEDIUM (301×127pt) ═══
    # 整体居中：标题行居中 + 卡片组居中
    with w.vstack(spacing=0, align="center"):
        w.spacer()  # 顶部弹性
        
        # 顶部标题行 - 居中
        with w.hstack(spacing=6, align="center"):
            w.icon("fuelpump.fill", size=14, color=ACCENT_COLOR)
            w.text(f"{current_city}今日油价", size=14, weight="semibold",
                   color=TITLE_COLOR)
            w.spacer()
            if data_ok and oil_data and oil_data.get("update"):
                update_date = oil_data.get("update", "")
                try:
                    date_str = datetime.datetime.strptime(update_date[:10], "%Y-%m-%d").strftime("%m-%d")
                except:
                    date_str = update_date[:10]
                w.text(date_str, size=11, color=SUB_COLOR)
            else:
                w.text("加载中", size=11, color=ERROR_COLOR)
        
        w.spacer()  # 弹性撑开
        
        # 主数据区 - 三列卡片居中
        if data_ok and oil_data:
            price92 = oil_data.get("price92", 0)
            price95 = oil_data.get("price95", 0)
            price98 = oil_data.get("price98", 0)
            
            with w.hstack(spacing=6, align="center"):
                # 左侧 92号
                with w.card(background=CARD_BG, corner_radius=10, 
                            padding=10, spacing=0):
                    with w.vstack(spacing=2, align="center"):
                        w.text("92#", size=11, weight="semibold", color=SUB_COLOR)
                        w.text(f"¥{price92:.2f}", size=20, weight="bold",
                               design="rounded", color=TITLE_COLOR)
                        w.text("元/升", size=9, color=SUB_COLOR)
                
                # 中间 95号
                with w.card(background=CARD_BG, corner_radius=10,
                            padding=10, spacing=0):
                    with w.vstack(spacing=2, align="center"):
                        w.text("95#", size=11, weight="semibold", color=SUB_COLOR)
                        w.text(f"¥{price95:.2f}", size=20, weight="bold",
                               design="rounded", color=TITLE_COLOR)
                        w.text("元/升", size=9, color=SUB_COLOR)
                
                # 右侧 98号
                with w.card(background=CARD_BG, corner_radius=10,
                            padding=10, spacing=0):
                    with w.vstack(spacing=2, align="center"):
                        w.text("98#", size=11, weight="semibold", color=SUB_COLOR)
                        w.text(f"¥{price98:.2f}", size=20, weight="bold",
                               design="rounded", color=TITLE_COLOR)
                        w.text("元/升", size=9, color=SUB_COLOR)
        else:
            # 网络异常时显示错误提示
            with w.card(background=CARD_BG, corner_radius=10,
                        padding=16, spacing=0):
                with w.vstack(spacing=4, align="center"):
                    w.icon("wifi.slash", size=24, color=ERROR_COLOR)
                    w.text("无法获取油价数据", size=13, weight="medium",
                           color=TEXT_COLOR)
                    w.text("请检查网络连接", size=11, color=SUB_COLOR)
        
        w.spacer()  # 底部弹性

else:
    # ═══ LARGE (301×317pt) ═══
    # 完整展示：头部+价格卡片+底部提示，全部居中
    with w.vstack(spacing=0, align="center"):
        w.spacer()  # 顶部弹性
        
        # 头部标题区 - 居中
        with w.hstack(spacing=6, align="center"):
            w.icon("fuelpump.fill", size=18, color=ACCENT_COLOR)
            w.text(f"{current_city}今日油价", size=18, weight="semibold",
                   color=TITLE_COLOR)
            w.spacer()
            if data_ok and oil_data and oil_data.get("update"):
                update_date = oil_data.get("update", "")
                try:
                    date_str = datetime.datetime.strptime(update_date[:10], "%Y-%m-%d").strftime("%m月%d日")
                except:
                    date_str = update_date[:10]
                w.text(date_str, size=12, color=SUB_COLOR)
            else:
                w.text("加载中", size=12, color=ERROR_COLOR)
        
        w.spacer(12)
        
        if data_ok and oil_data:
            price92 = oil_data.get("price92", 0)
            price95 = oil_data.get("price95", 0)
            price98 = oil_data.get("price98", 0)
            price0 = oil_data.get("price0", 0)
            update_date = oil_data.get("update", "")
            
            # 价格卡片区 - 2x2布局，全部居中
            with w.hstack(spacing=8, align="center"):
                # 92号卡片
                with w.card(background=CARD_BG, corner_radius=12, padding=12):
                    with w.vstack(spacing=2, align="center"):
                        w.text("92# 汽油", size=12, weight="medium", color=SUB_COLOR)
                        w.text(f"¥{price92:.2f}", size=26, weight="bold",
                               design="rounded", color=TITLE_COLOR)
                        w.text("元/升", size=10, color=SUB_COLOR)
                
                # 95号卡片
                with w.card(background=CARD_BG, corner_radius=12, padding=12):
                    with w.vstack(spacing=2, align="center"):
                        w.text("95# 汽油", size=12, weight="medium", color=SUB_COLOR)
                        w.text(f"¥{price95:.2f}", size=26, weight="bold",
                               design="rounded", color=TITLE_COLOR)
                        w.text("元/升", size=10, color=SUB_COLOR)
            
            w.spacer(8)
            
            with w.hstack(spacing=8, align="center"):
                # 98号卡片
                with w.card(background=CARD_BG, corner_radius=12, padding=12):
                    with w.vstack(spacing=2, align="center"):
                        w.text("98# 汽油", size=12, weight="medium", color=SUB_COLOR)
                        w.text(f"¥{price98:.2f}", size=26, weight="bold",
                               design="rounded", color=TITLE_COLOR)
                        w.text("元/升", size=10, color=SUB_COLOR)
                
                # 0号柴油卡片
                with w.card(background=CARD_BG, corner_radius=12, padding=12):
                    with w.vstack(spacing=2, align="center"):
                        w.text("0# 柴油", size=12, weight="medium", color=SUB_COLOR)
                        w.text(f"¥{price0:.2f}", size=26, weight="bold",
                               design="rounded", color=TITLE_COLOR)
                        w.text("元/升", size=10, color=SUB_COLOR)
            
            w.spacer()  # 弹性撑开
            
            # 底部提示区 - 居中
            with w.card(background=CARD_BG, corner_radius=10, padding=10):
                with w.hstack(spacing=8, align="center"):
                    w.icon("info.circle.fill", size=14, color=ACCENT_COLOR)
                    with w.vstack(spacing=1):
                        w.text("数据来源：油价查询接口", size=10, color=SUB_COLOR)
                        if update_date:
                            w.text(f"更新时间 {update_date}，实际价格以加油站为准",
                                   size=10, color=SUB_COLOR)
                        else:
                            w.text("实际价格以加油站为准",
                                   size=10, color=SUB_COLOR)
        else:
            # 网络异常时显示错误提示
            with w.card(background=CARD_BG, corner_radius=12, padding=20):
                with w.vstack(spacing=8, align="center"):
                    w.icon("wifi.slash", size=36, color=ERROR_COLOR)
                    w.text("无法获取油价数据", size=16, weight="semibold",
                           color=TEXT_COLOR)
                    w.text("请检查网络连接后刷新", size=12, color=SUB_COLOR)
            
            w.spacer()
            
            # 底部提示区
            with w.card(background=CARD_BG, corner_radius=10, padding=10):
                with w.hstack(spacing=8, align="center"):
                    w.icon("exclamationmark.triangle.fill", size=14, color=ERROR_COLOR)
                    with w.vstack(spacing=1):
                        w.text("提示", size=10, weight="medium", color=TEXT_COLOR)
                        w.text("确保网络连接正常，小组件将在下次刷新时重试",
                               size=10, color=SUB_COLOR)
        
        w.spacer()  # 底部弹性

# 渲染小组件
w.render()