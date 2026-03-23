# 2026-3-23 by.Silence 推荐使用stream进行抓包Cookie，抓包关键词query，复制curl即可，运行脚本自动解析Cookie。疯狂亏内x_x
import re
import os
import sys

try:
    import clipboard
    has_clip = True
except:
    has_clip = False

def validate_cookie(cookie_str):
    if not cookie_str or len(cookie_str) < 20:
        return False
    
    keywords = ["PvSessionId", "c_id", "ecs_token"]
    match_count = sum(1 for k in keywords if k in cookie_str)
    return match_count >= 1

def run_parser():
    raw_content = ""
    
    
    if has_clip:
        try:
            temp_data = clipboard.get()
            if temp_data and len(temp_data.strip()) > 50:
                raw_content = temp_data
        except:
            pass

    if not raw_content:
        print("系统剪贴板空值或数据长度异常")
        print("请手动粘贴抓包原始数据并回车:")
        raw_content = sys.stdin.read() if not sys.stdin.isatty() else input()

    if not raw_content or len(raw_content.strip()) < 10:
        print("终端输入数据校验未通过: 字符过短")
        return

    
    
    url_m = re.search(r"(?i)(https?://[^\s'\"]+)", raw_content)
    cookie_m = re.search(r"(?i)Cookie:\s*([^\r\n'\"]+)", raw_content)
    ua_m = re.search(r"(?i)User-Agent:\s*([^\r\n'\"]+)", raw_content)
    host_m = re.search(r"(?i)Host:\s*([^\r\n'\"]+)", raw_content)

    url = url_m.group(1) if url_m else "N/A"
    cookie = cookie_m.group(1) if cookie_m else ""
    ua = ua_m.group(1) if ua_m else "N/A"
    host = host_m.group(1).strip() if host_m else "m.client.10010.com"

    
    if not validate_cookie(cookie):
        print("\n[错误] 数据合法性校验失败")
        print("原因: 解析出的 Cookie 字段缺失或不符合联通接口特征")
        print("请检查抓包目标是否为 queryUserInfoSeven 接口")
        return

    
    result_map = {
        "URL": url,
        "HOST": host,
        "USER-AGENT": ua,
        "COOKIE": cookie
    }

    report = [
        "RAW DATA PARSE REPORT",
        "=" * 40,
        f"▷URL : {result_map['URL']}",
        f"▷HOST: {result_map['HOST']}",
        f"▷USER_AGENT : {result_map['USER-AGENT']}",
        "-" * 40,
        f"▷COOKIE:\n{result_map['COOKIE']}",
        "=" * 40,
        "获取成功: 接下来你需要自己手动复制粘贴这些数据到联通小组件里面，即可使用"
    ]

    final_report = "\n".join(report)
    
    try:
        with open("Cookie解析结果.txt", "w", encoding="utf-8") as f:
            f.write(final_report)
        print(final_report)
        print(f"\n解析结束，结果已同步至 PythonIDE 文档里面: Cookie解析结果.txt")
    except Exception as e:
        print(f"磁盘写入异常: {str(e)}")

if __name__ == "__main__":
    run_parser()
