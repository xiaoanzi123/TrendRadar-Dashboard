-- TrendRadar Dashboard 数据库表结构

-- 1. 平台表
CREATE TABLE IF NOT EXISTS platforms (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  url TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. 新闻条目表
CREATE TABLE IF NOT EXISTS news_items (
  id SERIAL PRIMARY KEY,
  platform_id TEXT REFERENCES platforms(id),
  title TEXT NOT NULL,
  url TEXT,
  rank INTEGER,
  hot_value TEXT,
  last_crawl_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. 排名历史表
CREATE TABLE IF NOT EXISTS rank_history (
  id SERIAL PRIMARY KEY,
  news_item_id INTEGER REFERENCES news_items(id) ON DELETE CASCADE,
  rank INTEGER NOT NULL,
  hot_value TEXT,
  crawl_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. RSS 订阅源表
CREATE TABLE IF NOT EXISTS rss_feeds (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  category TEXT,
  is_active BOOLEAN DEFAULT true,
  last_fetch_time TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. RSS 条目表
CREATE TABLE IF NOT EXISTS rss_items (
  id SERIAL PRIMARY KEY,
  feed_id TEXT REFERENCES rss_feeds(id),
  title TEXT NOT NULL,
  link TEXT,
  description TEXT,
  pub_date TIMESTAMP WITH TIME ZONE,
  author TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_news_items_platform_id ON news_items(platform_id);
CREATE INDEX IF NOT EXISTS idx_news_items_last_crawl_time ON news_items(last_crawl_time DESC);
CREATE INDEX IF NOT EXISTS idx_rank_history_news_item_id ON rank_history(news_item_id);
CREATE INDEX IF NOT EXISTS idx_rank_history_crawl_time ON rank_history(crawl_time);
CREATE INDEX IF NOT EXISTS idx_rss_items_feed_id ON rss_items(feed_id);
CREATE INDEX IF NOT EXISTS idx_rss_items_pub_date ON rss_items(pub_date DESC);

-- 插入一些示例平台数据
INSERT INTO platforms (id, name, url, is_active) VALUES
  ('weibo', '微博热搜', 'https://weibo.com', true),
  ('zhihu', '知乎热榜', 'https://zhihu.com', true),
  ('douyin', '抖音热点', 'https://douyin.com', true),
  ('bilibili', 'B站热门', 'https://bilibili.com', true),
  ('baidu', '百度热搜', 'https://baidu.com', true)
ON CONFLICT (id) DO NOTHING;

-- 启用 Row Level Security (RLS)
ALTER TABLE platforms ENABLE ROW LEVEL SECURITY;
ALTER TABLE news_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE rank_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE rss_feeds ENABLE ROW LEVEL SECURITY;
ALTER TABLE rss_items ENABLE ROW LEVEL SECURITY;

-- 创建公开读取策略（允许匿名用户读取数据）
CREATE POLICY "Allow public read access on platforms" ON platforms FOR SELECT USING (true);
CREATE POLICY "Allow public read access on news_items" ON news_items FOR SELECT USING (true);
CREATE POLICY "Allow public read access on rank_history" ON rank_history FOR SELECT USING (true);
CREATE POLICY "Allow public read access on rss_feeds" ON rss_feeds FOR SELECT USING (true);
CREATE POLICY "Allow public read access on rss_items" ON rss_items FOR SELECT USING (true);
