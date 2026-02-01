from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        # 设置 CORS 头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        # 路由处理
        if path == '/api/rss/feeds':
            response = self.get_feeds()
        elif path == '/api/rss/items':
            response = self.get_items(query_params)
        else:
            response = {'error': 'Not found'}

        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())

    def do_OPTIONS(self):
        """处理 OPTIONS 请求 (CORS 预检)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def get_feeds(self):
        """获取 RSS 订阅源列表"""
        # TODO: 实现从 Supabase 查询
        return {
            'data': [
                {
                    'id': 'hacker-news',
                    'name': 'Hacker News',
                    'url': 'https://hnrss.org/frontpage',
                    'enabled': True
                },
                {
                    'id': 'ruanyifeng',
                    'name': '阮一峰的网络日志',
                    'url': 'http://www.ruanyifeng.com/blog/atom.xml',
                    'enabled': True
                }
            ]
        }

    def get_items(self, params):
        """获取 RSS 条目"""
        feed_id = params.get('feed_id', [None])[0]
        limit = int(params.get('limit', [50])[0])

        # TODO: 实现从 Supabase 查询
        return {
            'data': [
                {
                    'id': 1,
                    'feed_id': 'hacker-news',
                    'feed_name': 'Hacker News',
                    'title': 'Sample RSS Item',
                    'link': 'https://example.com',
                    'published_at': '2025-01-27T10:00:00Z',
                    'summary': 'This is a sample RSS item',
                    'created_at': '2025-01-27T10:00:00Z'
                }
            ]
        }
