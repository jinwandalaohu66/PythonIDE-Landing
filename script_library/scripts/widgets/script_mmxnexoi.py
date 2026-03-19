# 欢迎使用 PythonIDE！如果觉得好用，请给个好评哦～
import requests
from widget import Widget, family
from widget import SMALL, MEDIUM, LARGE, CIRCULAR, RECTANGULAR


def get_unicom_data():

    url = ''
    headers = {
        'Host': '',
        'User-Agent': '',
        'Cookie': 
#这里把你抓到的cookie放里面即可.
'这里....'
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            flow = data.get('flowResource', {}).get('flowPersent', '0')
            fee = data.get('feeResource', {}).get('feePersent', '0')
            voice = data.get('voiceResource', {}).get('voicePersent', '0')
            t = data.get("flush_date_time", "").split(" ")[-1] if " " in data.get("flush_date_time", "") else "刚刚"
            return True, flow, fee, voice, t
    except:
        pass
    return False, "0", "0", "0", "--"


success, flow, fee, voice, update_time = get_unicom_data()


w = Widget(
    background=("#FFFFFF", "#0B0F1A"), # 
    padding=16
)

if family == MEDIUM:
    
    with w.hstack(spacing=0):
        
        
        with w.vstack(align="leading", spacing=0):
            
            with w.hstack(spacing=6):
                w.icon("antenna.radiowaves.left.and.right", size=16, color="#E63946")
                w.text("中国联通", size=14, weight="bold", color=("#111", "#EEE"))
            
            w.spacer(14)
            w.text("剩余通用流量", size=12, color=("#64748B", "#94A3B8"))
            w.spacer(4)
            
            
            with w.hstack(spacing=4, align="bottom"):
                
                w.text(flow, size=36, weight="bold", design="rounded", color=("#000", "#FFF"))
                
                w.text("GB", size=14, weight="bold", color="#E63946")

        
        w.spacer()

        
        with w.vstack(align="leading", spacing=10):
            w.spacer(6) 
            
            
            with w.hstack(spacing=8):
                w.icon("yensign.circle.fill", size=14, color="#F59E0B")
                w.text(f"{fee} 元", size=11, weight="semibold", color="#F59E0B")
            
           
            with w.hstack(spacing=8):
                w.icon("phone.fill", size=14, color="#10B981")
                w.text(f"{voice} 分钟", size=11, weight="semibold", color="#10B981")
            
            
            with w.hstack(spacing=8):
                w.icon("clock", size=14, color=("#94A3B8", "#64748B"))
                w.text(update_time, size=11, color=("#94A3B8", "#64748B"))


w.render()
#2026-3-19