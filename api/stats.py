from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import os

# Supabase 配置
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')

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
        if path == '/api/stats/platforms':
            response = self.get_platform_stats(query_params)
        elif path == '/api/stats/keywords':
            response = self.get_keyword_stats(query_params)
        elif path == '/api/stats/trends':
            response = self.get_trend_data(query_params)
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

    def get_platform_stats(self, params):
        """获取平台统计数据"""
        # TODO: 实现从 Supabase 查询
        return {
            'data': [
                {
                    'platform_id': 'weibo',
                    'platform_name': '微博',
                    'total_items': 50,
                    'avg_rank': 25,
                    'top_keywords': ['热点', '新闻', '科技']
                },
                {
                    'platform_id': 'zhihu',
                    'platform_name': '知乎',
                    'total_items': 45,
                    'avg_rank': 22,
                    'top_keywords': ['问答', '技术', '生活']
                }
            ]
        }

    def get_keyword_stats(self, params):
        """获取关键词统计数据"""
        # TODO: 实现从 Supabase 查询
        return {
            'data': [
                {
                    'keyword': 'AI',
                    'count': 120,
                    'platforms': ['weibo', 'zhihu', 'toutiao'],
                    'news_items': []
                },
                {
                    'keyword': '科技',
                    'count': 95,
                    'platforms': ['toutiao', 'ithome'],
                    'news_items': []
                }
            ]
        }

    def get_trend_data(self, params):
        """获取趋势数据"""
        days = int(params.get('days', [7])[0])
        # TODO: 实现从 Supabase 查询
        return {
            'data': [
                {
                    'date': '2025-01-26',
                    'count': 150,
                    'platforms': {'weibo': 50, 'zhihu': 45, 'toutiao': 55}
                },
                {
                    'date': '2025-01-27',
                    'count': 165,
                    'platforms': {'weibo': 55, 'zhihu': 50, 'toutiao': 60}
                }
            ]
        }
