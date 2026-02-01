#!/usr/bin/env python3
"""
TrendRadar 数据爬虫
从各大平台抓取热点数据并存入 Supabase
"""

import os
import sys
import json
import time
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values

# 支持的平台配置
PLATFORMS = {
    'weibo': {'name': '微博热搜', 'api': 'weibo'},
    'zhihu': {'name': '知乎热榜', 'api': 'zhihu'},
    'douyin': {'name': '抖音热榜', 'api': 'douyin'},
    'bilibili': {'name': 'B站热门', 'api': 'bilibili'},
    'baidu': {'name': '百度热搜', 'api': 'baidu'},
    'toutiao': {'name': '今日头条', 'api': 'toutiao'},
    '36kr': {'name': '36氪', 'api': '36kr'},
    'sspai': {'name': '少数派', 'api': 'sspai'},
}

def get_database_connection():
    """获取数据库连接"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL 环境变量未设置")

    return psycopg2.connect(db_url)

def fetch_platform_data(platform_id):
    """
    从 NewsNow API 获取平台数据
    API 文档: https://github.com/newsnow/api
    """
    try:
        import requests

        # NewsNow API 端点
        api_url = f"https://api.newsnow.com/v1/{PLATFORMS[platform_id]['api']}/hot"

        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        data = response.json()

        # 解析数据（根据实际 API 响应格式调整）
        items = []
        if 'data' in data:
            for idx, item in enumerate(data['data'][:20], 1):  # 只取前20条
                items.append({
                    'platform_id': platform_id,
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'rank': idx,
                    'hot_value': str(item.get('hot', '')),
                })

        return items

    except Exception as e:
        print(f"❌ 获取 {platform_id} 数据失败: {e}")
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

    for platform_id in PLATFORMS.keys():
        print(f"正在爬取: {PLATFORMS[platform_id]['name']}...")

        items = fetch_platform_data(platform_id)

        if items:
            update_database(conn, items)
            total_items += len(items)

        # 避免请求过快
        time.sleep(1)

    conn.close()

    print(f"\n{'='*50}")
    print(f"✓ 爬取完成！共获取 {total_items} 条数据")
    print(f"{'='*50}\n")

if __name__ == '__main__':
    try:
        crawl_all_platforms()
    except Exception as e:
        print(f"❌ 爬虫运行失败: {e}")
        sys.exit(1)
