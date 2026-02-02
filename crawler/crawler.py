#!/usr/bin/env python3
"""
TrendRadar Dashboard 数据爬虫
基于 TrendRadar 项目的实现，使用 NewsNow API 获取热榜数据
"""

import os
import sys
import json
import time
import random
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values

try:
    import requests
except ImportError:
    print("请安装依赖: pip install requests")
    sys.exit(1)

# NewsNow API 配置
API_BASE = "https://newsnow.busiyi.world/api/s"

# 支持的平台配置（基于 TrendRadar）
PLATFORMS = {
    'weibo': {'name': '微博热搜', 'api_id': 'weibo'},
    'zhihu': {'name': '知乎热榜', 'api_id': 'zhihu'},
    'douyin': {'name': '抖音热榜', 'api_id': 'douyin'},
    'bilibili': {'name': 'B站热搜', 'api_id': 'bilibili-hot-search'},
    'baidu': {'name': '百度热搜', 'api_id': 'baidu'},
    'toutiao': {'name': '今日头条', 'api_id': 'toutiao'},
}

def get_database_connection():
    """获取数据库连接"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL 环境变量未设置")
    return psycopg2.connect(db_url)

def fetch_platform_data(platform_id, max_retries=3):
    """
    从 NewsNow API 获取平台数据
    参考 TrendRadar 的实现
    """
    config = PLATFORMS.get(platform_id)
    if not config:
        return []

    api_id = config['api_id']
    url = f"{API_BASE}?id={api_id}&latest"

    # 模拟浏览器请求头（参考 TrendRadar）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://newsnow.busiyi.world/',
        'Origin': 'https://newsnow.busiyi.world',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    for attempt in range(max_retries):
        try:
            # 添加随机延迟（3-5秒）
            if attempt > 0:
                delay = random.uniform(3, 5)
                print(f"  重试 {attempt}/{max_retries}，等待 {delay:.1f}秒...")
                time.sleep(delay)

            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            data = response.json()

            # 解析数据
            items = []
            if isinstance(data, dict) and 'items' in data:
                for item in data['items'][:20]:  # 只取前20条
                    title = item.get('title')
                    if not title or isinstance(title, (float, int)) or not title.strip():
                        continue

                    items.append({
                        'platform_id': platform_id,
                        'title': title.strip(),
                        'url': item.get('url', item.get('mobileUrl', '')),
                        'rank': item.get('rank', 0),
                        'hot_value': str(item.get('extra', {}).get('hot', '')),
                    })

            return items

        except requests.exceptions.RequestException as e:
            print(f"  请求失败: {e}")
            if attempt == max_retries - 1:
                print(f"❌ {config['name']} 获取失败（已重试 {max_retries} 次）")
                return []

        except json.JSONDecodeError as e:
            print(f"  JSON 解析失败: {e}")
            return []

        except Exception as e:
            print(f"  未知错误: {e}")
            return []

    return []

def update_database(conn, items):
    """更新数据库"""
    if not items:
        return

    cursor = conn.cursor()

    try:
        platform_id = items[0]['platform_id']

        # 删除该平台的旧数据（保留最近24小时的历史）
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
        import traceback
        traceback.print_exc()

    finally:
        cursor.close()

def crawl_all_platforms():
    """爬取所有平台数据"""
    print(f"\n{'='*60}")
    print(f"TrendRadar Dashboard 数据爬虫")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    conn = get_database_connection()
    total_items = 0
    success_count = 0
    fail_count = 0

    for platform_id, config in PLATFORMS.items():
        print(f"正在爬取: {config['name']} ({platform_id})...")

        items = fetch_platform_data(platform_id)

        if items:
            update_database(conn, items)
            total_items += len(items)
            success_count += 1
        else:
            fail_count += 1

        # 请求间隔（100ms + 随机偏差）
        time.sleep(0.1 + random.uniform(0, 0.05))

    conn.close()

    print(f"\n{'='*60}")
    print(f"✓ 爬取完成！")
    print(f"  成功: {success_count}/{len(PLATFORMS)} 个平台")
    print(f"  失败: {fail_count}/{len(PLATFORMS)} 个平台")
    print(f"  数据: 共获取 {total_items} 条")
    print(f"  结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    try:
        crawl_all_platforms()
    except Exception as e:
        print(f"\n❌ 爬虫运行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
