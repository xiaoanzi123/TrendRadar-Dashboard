#!/usr/bin/env python3
"""
TrendRadar 数据爬虫 v2
使用网页爬取方式获取热点数据
"""

import os
import sys
import json
import time
import re
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("请安装依赖: pip install requests beautifulsoup4")
    sys.exit(1)

# 支持的平台配置
PLATFORMS = {
    'weibo': {'name': '微博热搜', 'enabled': True},
    'zhihu': {'name': '知乎热榜', 'enabled': True},
    'bilibili': {'name': 'B站热门', 'enabled': True},
    'baidu': {'name': '百度热搜', 'enabled': True},
}

def get_database_connection():
    """获取数据库连接"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL 环境变量未设置")
    return psycopg2.connect(db_url)

def fetch_weibo_hot():
    """爬取微博热搜"""
    try:
        # 使用微博热搜榜页面
        url = "https://s.weibo.com/top/summary"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        items = []

        # 查找热搜列表
        hot_list = soup.find_all('td', class_='td-02')

        for idx, item in enumerate(hot_list[:20], 1):
            link = item.find('a')
            if link:
                title = link.get_text(strip=True)
                href = link.get('href', '')

                # 获取热度值
                hot_span = item.find_next('td', class_='td-03')
                hot_value = hot_span.get_text(strip=True) if hot_span else ''

                items.append({
                    'platform_id': 'weibo',
                    'title': title,
                    'url': f"https://s.weibo.com{href}" if href else '',
                    'rank': idx,
                    'hot_value': hot_value,
                })

        return items
    except Exception as e:
        print(f"❌ 微博爬取失败: {e}")
        return []

def fetch_zhihu_hot():
    """爬取知乎热榜"""
    try:
        # 使用知乎 API
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        items = []
        for idx, item in enumerate(data.get('data', [])[:20], 1):
            target = item.get('target', {})
            items.append({
                'platform_id': 'zhihu',
                'title': target.get('title', ''),
                'url': target.get('url', ''),
                'rank': idx,
                'hot_value': str(item.get('detail_text', '')),
            })

        return items
    except Exception as e:
        print(f"❌ 知乎爬取失败: {e}")
        return []

def fetch_bilibili_hot():
    """爬取B站热门"""
    try:
        # 使用B站热门视频 API
        url = "https://api.bilibili.com/x/web-interface/popular"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        items = []
        if data.get('code') == 0:
            for idx, item in enumerate(data.get('data', {}).get('list', [])[:20], 1):
                items.append({
                    'platform_id': 'bilibili',
                    'title': item.get('title', ''),
                    'url': item.get('short_link_v2', ''),
                    'rank': idx,
                    'hot_value': str(item.get('stat', {}).get('view', '')),
                })

        return items
    except Exception as e:
        print(f"❌ B站爬取失败: {e}")
        return []

def fetch_baidu_hot():
    """爬取百度热搜"""
    try:
        # 使用百度热搜榜
        url = "https://top.baidu.com/board?tab=realtime"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        # 从页面中提取数据（百度热搜数据在 JS 中）
        pattern = r'<!--s-data:(.*?)-->'
        match = re.search(pattern, response.text)

        items = []
        if match:
            data = json.loads(match.group(1))
            cards = data.get('data', {}).get('cards', [])

            for card in cards:
                if card.get('type') == 'toplist1':
                    for idx, item in enumerate(card.get('content', [])[:20], 1):
                        items.append({
                            'platform_id': 'baidu',
                            'title': item.get('word', ''),
                            'url': item.get('url', ''),
                            'rank': idx,
                            'hot_value': str(item.get('hotScore', '')),
                        })
                    break

        return items
    except Exception as e:
        print(f"❌ 百度爬取失败: {e}")
        return []

def fetch_platform_data(platform_id):
    """根据平台ID获取数据"""
    fetchers = {
        'weibo': fetch_weibo_hot,
        'zhihu': fetch_zhihu_hot,
        'bilibili': fetch_bilibili_hot,
        'baidu': fetch_baidu_hot,
    }

    fetcher = fetchers.get(platform_id)
    if fetcher:
        return fetcher()
    return []

def update_database(conn, items):
    """更新数据库"""
    if not items:
        return

    cursor = conn.cursor()

    try:
        # 删除该平台的旧数据（保留最近24小时的历史）
        platform_id = items[0]['platform_id']
        cursor.execute("""
            DELETE FROM news_items
            WHERE platform_id = %s
            AND last_crawl_time < NOW() - INTERVAL '24 hours'
        """, (platform_id,))

        # 插入新数据
        insert_query = """
            INSERT INTO news_items (platform_id, title, url, rank, hot_value, last_crawl_time)
            VALUES %s
            ON CONFLICT (platform_id, title)
            DO UPDATE SET
                rank = EXCLUDED.rank,
                hot_value = EXCLUDED.hot_value,
                last_crawl_time = EXCLUDED.last_crawl_time
        """

        values = [
            (
                item['platform_id'],
                item['title'],
                item['url'],
                item['rank'],
                item['hot_value'],
                datetime.now()
            )
            for item in items
        ]

        execute_values(cursor, insert_query, values)
        conn.commit()

        print(f"✓ {platform_id}: 成功更新 {len(items)} 条数据")

    except Exception as e:
        conn.rollback()
        print(f"❌ 数据库更新失败: {e}")

    finally:
        cursor.close()

def crawl_all_platforms():
    """爬取所有平台数据"""
    print(f"\n{'='*50}")
    print(f"开始爬取数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    conn = get_database_connection()
    total_items = 0

    for platform_id, config in PLATFORMS.items():
        if not config.get('enabled'):
            continue

        print(f"正在爬取: {config['name']}...")

        items = fetch_platform_data(platform_id)

        if items:
            update_database(conn, items)
            total_items += len(items)

        # 避免请求过快
        time.sleep(2)

    conn.close()

    print(f"\n{'='*50}")
    print(f"✓ 爬取完成！共获取 {total_items} 条数据")
    print(f"{'='*50}\n")

if __name__ == '__main__':
    try:
        crawl_all_platforms()
    except Exception as e:
        print(f"❌ 爬虫运行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
