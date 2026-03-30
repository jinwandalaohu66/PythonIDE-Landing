import requests
import json

def query_ip_info(ip_address):
    """
    高精度IP查询工具箱
    查询指定IP地址的详细信息
    
    参数:
        ip_address (str): 要查询的IP地址
    
    返回:
        dict: 包含IP详细信息的字典
    """
    url = "https://api.ip77.net/ip2/v4/"
    
    payload = {'ip': ip_address}
    
    headers = {
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'sec-fetch-site': "cross-site",
        'accept-language': "zh-CN,zh-Hans;q=0.9",
        'sec-fetch-mode': "cors",
        'origin': "https://uutool.cn",
        'referer': "https://uutool.cn/",
        'sec-fetch-dest': "empty"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('code') == 0:
            ip_data = data['data']
            result = {
                '归属地': f"{ip_data.get('country', '')}{ip_data.get('province', '')}{ip_data.get('city', '')}{ip_data.get('district', '')}{ip_data.get('street', '')}",
                '运营商': ip_data.get('isp', ''),
                '基本信息': {
                    'IP地址': ip_data.get('ip', ''),
                    '数字地址': ip_data.get('ip_int', ''),
                    '洲': ip_data.get('continent', ''),
                    '国家': ip_data.get('country', ''),
                    '省份': ip_data.get('province', ''),
                    '城市': ip_data.get('city', ''),
                    '区县': ip_data.get('district', ''),
                    '街道': ip_data.get('street', ''),
                    '区划编码': ip_data.get('area_code', ''),
                    '邮政编码': ip_data.get('zip_code', ''),
                    '经度': ip_data.get('longitude', ''),
                    '纬度': ip_data.get('latitude', ''),
                    '时区': ip_data.get('time_zone', '')
                },
                '街道定位历史': [f"历史{i+1} {address}" for i, address in enumerate(ip_data.get('street_history', []))],
                'IP风险信息': {
                    'IP地址': ip_data.get('ip', ''),
                    '风险分数': ip_data.get('risk', {}).get('risk_score', ''),
                    '风险等级': ip_data.get('risk', {}).get('risk_level', ''),
                    '是否为代理': ip_data.get('risk', {}).get('is_proxy', ''),
                    '代理类型': ip_data.get('risk', {}).get('proxy_type', ''),
                    '风险标签': ip_data.get('risk', {}).get('risk_tag', '')
                }
            }
            return result
        else:
            return {'error': f'API返回错误: {data.get("message", "未知错误")}'}
            
    except requests.exceptions.RequestException as e:
        return {'error': f'网络请求失败: {str(e)}'}
    except json.JSONDecodeError as e:
        return {'error': f'JSON解析失败: {str(e)}'}
    except Exception as e:
        return {'error': f'未知错误: {str(e)}'}

def format_ip_info(ip_info):
    """
    格式化IP查询结果
    
    参数:
        ip_info (dict): IP查询结果字典
    
    返回:
        str: 格式化的查询结果
    """
    if 'error' in ip_info:
        return f"查询失败: {ip_info['error']}"
    
    output = []
    output.append("=" * 50)
    output.append("高精度IP查询结果")
    output.append("=" * 50)
    
    # 基础信息
    output.append(f"归属地: {ip_info.get('归属地', '')}")
    output.append(f"运营商: {ip_info.get('运营商', '')}")
    
    # 详细信息
    output.append("\n详细信息:")
    output.append("-" * 30)
    basic_info = ip_info.get('基本信息', {})
    for key, value in basic_info.items():
        if value:  # 只显示有值的信息
            output.append(f"{key}: {value}")
    
    # 街道定位历史
    output.append("\n街道定位历史:")
    output.append("-" * 30)
    for history in ip_info.get('街道定位历史', []):
        output.append(history)
    
    # IP风险信息
    output.append("\nIP风险信息:")
    output.append("-" * 30)
    risk_info = ip_info.get('IP风险信息', {})
    for key, value in risk_info.items():
        if value or str(value) == "0":  # 显示有值或为0的字段
            output.append(f"{key}: {value}")
    
    output.append("=" * 50)
    return "\n".join(output)

def main():
    """主函数"""
    print("高精度IP查询工具箱")
    print("-" * 30)
    
    while True:
        ip = input("请输入要查询的IP地址（输入'quit'退出）: ").strip()
        
        if ip.lower() in ['quit', 'exit', 'q']:
            print("感谢使用，再见！")
            break
        
        if not ip:
            print("IP地址不能为空，请重新输入！")
            continue
        
        print(f"\n正在查询IP: {ip}")
        print("查询中，请稍候...")
        
        result = query_ip_info(ip)
        formatted_result = format_ip_info(result)
        
        print(f"\n{formatted_result}\n")

if __name__ == "__main__":
    main()
