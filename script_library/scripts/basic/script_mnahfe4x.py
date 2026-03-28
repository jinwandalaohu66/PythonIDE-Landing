#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
爬取谷歌热点新闻
使用 RSS 订阅源获取最新新闻
"""

import requests
import xml.etree.ElementTree as ET
import time
from datetime import datetime
import sys

def fetch_google_news(rss_url="https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans"):
    """
    从 Google News RSS 订阅源获取热点新闻
    
    Args:
        rss_url (str): Google News RSS 订阅源 URL
        
    Returns:
        list: 新闻条目列表，每个条目包含标题、链接、发布时间等信息
    """
    print("正在获取谷歌热点新闻...")
    
    try:
        # 设置请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        }
        
        # 发送请求获取 RSS 数据
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析 XML
        root = ET.fromstring(response.content)
        
        # XML 命名空间处理
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'media': 'http://search.yahoo.com/mrss/'
        }
        
        # 查找所有 item 元素
        items = root.findall('.//item')
        
        if not items:
            # 尝试另一种查找方式
            items = root.findall('.//channel/item')
            
        if not items:
            print("未获取到新闻条目")
            return []
        
        print(f"成功获取到 {len(items)} 条新闻\n")
        
        # 提取新闻信息
        news_items = []
        for i, item in enumerate(items[:20], 1):  # 限制显示前20条
            # 获取标题
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else '无标题'
            
            # 获取链接
            link_elem = item.find('link')
            link = link_elem.text if link_elem is not None else '#'
            
            # 获取发布时间
            pub_date_elem = item.find('pubDate')
            if pub_date_elem is None:
                pub_date_elem = item.find('dc:date', namespaces)
            published = pub_date_elem.text if pub_date_elem is not None else ''
            
            # 获取描述/摘要
            desc_elem = item.find('description')
            if desc_elem is None:
                desc_elem = item.find('content:encoded', namespaces)
            summary = ''
            if desc_elem is not None and desc_elem.text:
                summary = desc_elem.text[:200]
            
            # 获取来源
            source_elem = item.find('source')
            source = source_elem.text if source_elem is not None else ''
            
            # 构建新闻项
            news_item = {
                'index': i,
                'title': title,
                'link': link,
                'published': published,
                'summary': summary,
                'source': source
            }
            news_items.append(news_item)
        
        return news_items
    
    except requests.RequestException as e:
        print(f"网络请求失败: {e}")
        return []
    except ET.ParseError as e:
        print(f"XML 解析失败: {e}")
        return []
    except Exception as e:
        print(f"获取新闻失败: {e}")
        return []

def display_news(news_items):
    """格式化显示新闻"""
    if not news_items:
        print("没有新闻可显示")
        return
    
    print("=" * 80)
    print(f"📰 谷歌热点新闻 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print("=" * 80)
    
    for item in news_items:
        print(f"\n{item['index']}. {item['title']}")
        
        if item['source']:
            print(f"   来源: {item['source']}")
        
        if item['published']:
            # 发布时间可能包含时间格式信息，直接显示
            print(f"   时间: {item['published']}")
        
        if item['summary']:
            print(f"   摘要: {item['summary']}...")
        
        print(f"   链接: {item['link']}")
        print("-" * 60)

def get_news_by_category():
    """按类别获取新闻"""
    categories = {
        '1': ('综合', 'https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
        '2': ('国际', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
        '3': ('科技', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKQ1VpZ0FQAQ?hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
        '4': ('商业', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKQ1VpZ0FQAQ?hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
        '5': ('娱乐', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNREpxYW5RU0JXVnVMVWRDR2dKQ1VpZ0FQAQ?hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
        '6': ('体育', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JXVnVMVWRDR2dKQ1VpZ0FQAQ?hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
        '7': ('健康', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDR2dKQ1VpZ0FQAQ?hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
    }
    
    print("\n请选择新闻类别:")
    for key, (name, _) in categories.items():
        print(f"  {key}. {name}")
    print("  0. 综合新闻 (默认)")
    
    choice = input("\n请输入数字选择类别 (默认: 0): ").strip()
    
    if choice in categories:
        category_name, rss_url = categories[choice]
        print(f"\n正在获取「{category_name}」类别新闻...")
        return rss_url
    else:
        print("\n正在获取综合新闻...")
        return categories['1'][1]  # 默认返回综合新闻 URL

def main():
    """主函数"""
    print("=" * 80)
    print("📰 谷歌热点新闻爬取工具")
    print("=" * 80)
    
    # 获取用户选择的类别
    rss_url = get_news_by_category()
    
    # 获取新闻
    news_items = fetch_google_news(rss_url)
    
    # 显示新闻
    if news_items:
        display_news(news_items)
        
        # 保存到文件选项
        save_option = input("\n是否将新闻保存到文件? (y/N): ").strip().lower()
        if save_option == 'y':
            save_to_file(news_items)
    else:
        print("未能获取到新闻，请检查网络连接或稍后重试")

def save_to_file(news_items):
    """将新闻保存到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"谷歌新闻_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"谷歌热点新闻 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
            f.write("=" * 80 + "\n\n")
            
            for item in news_items:
                f.write(f"{item['index']}. {item['title']}\n")
                
                if item['source']:
                    f.write(f"   来源: {item['source']}\n")
                
                if item['published']:
                    f.write(f"   时间: {item['published']}\n")
                
                if item['summary']:
                    f.write(f"   摘要: {item['summary']}...\n")
                
                f.write(f"   链接: {item['link']}\n")
                f.write("-" * 60 + "\n\n")
        
        print(f"✓ 新闻已保存到文件: {filename}")
    except Exception as e:
        print(f"✗ 保存文件失败: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        sys.exit(1)