#!/usr/bin/env python3
"""
TrendRadar SQLite 到 Supabase PostgreSQL 数据迁移脚本

使用方法:
    python migrate_to_supabase.py --sqlite-db output/news/2025-01-27.db --supabase-url https://xxx.supabase.co --supabase-key your-key

依赖:
    pip install psycopg2-binary python-dotenv
"""

import sqlite3
import argparse
import os
from datetime import datetime
from typing import Optional
import psycopg2
from psycopg2.extras import execute_batch


def parse_args():
    parser = argparse.ArgumentParser(description='迁移 TrendRadar 数据到 Supabase')
    parser.add_argument('--sqlite-db', required=True, help='SQLite 数据库文件路径')
    parser.add_argument('--supabase-url', required=True, help='Supabase 项目 URL')
    parser.add_argument('--supabase-key', required=True, help='Supabase 服务密钥')
    parser.add_argument('--batch-size', type=int, default=100, help='批量插入大小')
    return parser.parse_args()


def get_pg_connection(supabase_url: str, supabase_key: str):
    """创建 PostgreSQL 连接"""
    # 从 Supabase URL 提取数据库连接信息
    # 格式: https://xxx.supabase.co -> db.xxx.supabase.co
    host = supabase_url.replace('https://', 'db.').replace('http://', 'db.')

    conn = psycopg2.connect(
        host=host,
        database="postgres",
        user="postgres",
        password=supabase_key,
        port=5432
    )
    return conn


def migrate_platforms(sqlite_cursor, pg_cursor, batch_size=100):
    """迁移平台数据"""
    print("迁移平台数据...")

    sqlite_cursor.execute("SELECT id, name, is_active, updated_at FROM platforms")
    platforms = sqlite_cursor.fetchall()

    if not platforms:
        print("  没有平台数据需要迁移")
        return

    # 转换数据格式
    data = []
    for p in platforms:
        data.append((
            p[0],  # id
            p[1],  # name
            bool(p[2]),  # is_active
            p[3] if p[3] else datetime.now().isoformat()  # updated_at
        ))

    # 批量插入
    execute_batch(
        pg_cursor,
        """INSERT INTO platforms (id, name, is_active, updated_at)
           VALUES (%s, %s, %s, %s)
           ON CONFLICT (id) DO UPDATE SET
           name = EXCLUDED.name,
           is_active = EXCLUDED.is_active,
           updated_at = EXCLUDED.updated_at""",
        data,
        page_size=batch_size
    )

    print(f"  ✓ 迁移了 {len(data)} 个平台")


def migrate_news_items(sqlite_cursor, pg_cursor, batch_size=100):
    """迁移新闻数据"""
    print("迁移新闻数据...")

    sqlite_cursor.execute("""
        SELECT title, platform_id, rank, url, mobile_url,
               first_crawl_time, last_crawl_time, crawl_count,
               created_at, updated_at
        FROM news_items
    """)

    news_items = sqlite_cursor.fetchall()

    if not news_items:
        print("  没有新闻数据需要迁移")
        return

    # 批量插入
    execute_batch(
        pg_cursor,
        """INSERT INTO news_items
           (title, platform_id, rank, url, mobile_url,
            first_crawl_time, last_crawl_time, crawl_count,
            created_at, updated_at)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        news_items,
        page_size=batch_size
    )

    print(f"  ✓ 迁移了 {len(news_items)} 条新闻")


def migrate_rank_history(sqlite_cursor, pg_cursor, batch_size=100):
    """迁移排名历史数据"""
    print("迁移排名历史...")

    # 注意: 需要映射 news_item_id
    # 这里简化处理，假设 ID 一致或跳过
    print("  ⚠️  排名历史迁移需要手动处理 ID 映射")


def migrate_rss_data(sqlite_cursor, pg_cursor, batch_size=100):
    """迁移 RSS 数据"""
    print("迁移 RSS 数据...")

    # 检查是否有 RSS 表
    sqlite_cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='rss_feeds'
    """)

    if not sqlite_cursor.fetchone():
        print("  没有 RSS 数据需要迁移")
        return

    # 迁移 RSS 订阅源
    sqlite_cursor.execute("SELECT id, name, url, enabled, max_age_days FROM rss_feeds")
    feeds = sqlite_cursor.fetchall()

    if feeds:
        execute_batch(
            pg_cursor,
            """INSERT INTO rss_feeds (id, name, url, enabled, max_age_days)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
               name = EXCLUDED.name,
               url = EXCLUDED.url,
               enabled = EXCLUDED.enabled,
               max_age_days = EXCLUDED.max_age_days""",
            feeds,
            page_size=batch_size
        )
        print(f"  ✓ 迁移了 {len(feeds)} 个 RSS 订阅源")


def main():
    args = parse_args()

    print("=" * 60)
    print("TrendRadar 数据迁移工具")
    print("=" * 60)
    print(f"SQLite 数据库: {args.sqlite_db}")
    print(f"Supabase URL: {args.supabase_url}")
    print("=" * 60)

    # 连接数据库
    print("\n连接数据库...")
    sqlite_conn = sqlite3.connect(args.sqlite_db)
    sqlite_cursor = sqlite_conn.cursor()

    pg_conn = get_pg_connection(args.supabase_url, args.supabase_key)
    pg_cursor = pg_conn.cursor()

    try:
        # 开始迁移
        print("\n开始迁移...\n")

        migrate_platforms(sqlite_cursor, pg_cursor, args.batch_size)
        migrate_news_items(sqlite_cursor, pg_cursor, args.batch_size)
        migrate_rss_data(sqlite_cursor, pg_cursor, args.batch_size)

        # 提交事务
        pg_conn.commit()

        print("\n" + "=" * 60)
        print("✓ 迁移完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 迁移失败: {e}")
        pg_conn.rollback()
        raise

    finally:
        sqlite_conn.close()
        pg_conn.close()


if __name__ == '__main__':
    main()
