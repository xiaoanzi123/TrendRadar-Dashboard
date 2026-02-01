-- TrendRadar Dashboard 数据库迁移脚本
-- 适用于 Supabase PostgreSQL

-- ============================================
-- 平台信息表
-- ============================================
CREATE TABLE IF NOT EXISTS platforms (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 新闻条目表
-- ============================================
CREATE TABLE IF NOT EXISTS news_items (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    platform_id TEXT NOT NULL REFERENCES platforms(id),
    rank INTEGER NOT NULL,
    url TEXT DEFAULT '',
    mobile_url TEXT DEFAULT '',
    first_crawl_time TIMESTAMP WITH TIME ZONE NOT NULL,
    last_crawl_time TIMESTAMP WITH TIME ZONE NOT NULL,
    crawl_count INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 标题变更历史表
-- ============================================
CREATE TABLE IF NOT EXISTS title_changes (
    id BIGSERIAL PRIMARY KEY,
    news_item_id BIGINT NOT NULL REFERENCES news_items(id),
    old_title TEXT NOT NULL,
    new_title TEXT NOT NULL,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 排名历史表
-- ============================================
CREATE TABLE IF NOT EXISTS rank_history (
    id BIGSERIAL PRIMARY KEY,
    news_item_id BIGINT NOT NULL REFERENCES news_items(id),
    rank INTEGER NOT NULL,
    crawl_time TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 抓取记录表
-- ============================================
CREATE TABLE IF NOT EXISTS crawl_records (
    id BIGSERIAL PRIMARY KEY,
    crawl_time TIMESTAMP WITH TIME ZONE NOT NULL UNIQUE,
    total_items INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 抓取来源状态表
-- ============================================
CREATE TABLE IF NOT EXISTS crawl_source_status (
    crawl_record_id BIGINT NOT NULL REFERENCES crawl_records(id),
    platform_id TEXT NOT NULL REFERENCES platforms(id),
    status TEXT NOT NULL CHECK(status IN ('success', 'failed')),
    PRIMARY KEY (crawl_record_id, platform_id)
);

-- ============================================
-- 推送记录表
-- ============================================
CREATE TABLE IF NOT EXISTS push_records (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    pushed BOOLEAN DEFAULT false,
    push_time TIMESTAMP WITH TIME ZONE,
    report_type TEXT,
    ai_analyzed BOOLEAN DEFAULT false,
    ai_analysis_time TIMESTAMP WITH TIME ZONE,
    ai_analysis_mode TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- RSS 订阅源表
-- ============================================
CREATE TABLE IF NOT EXISTS rss_feeds (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    enabled BOOLEAN DEFAULT true,
    max_age_days INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- RSS 条目表
-- ============================================
CREATE TABLE IF NOT EXISTS rss_items (
    id BIGSERIAL PRIMARY KEY,
    feed_id TEXT NOT NULL REFERENCES rss_feeds(id),
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE,
    summary TEXT,
    content TEXT,
    author TEXT,
    guid TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(feed_id, guid)
);

-- ============================================
-- 索引定义
-- ============================================

-- 平台索引
CREATE INDEX IF NOT EXISTS idx_news_platform ON news_items(platform_id);

-- 时间索引
CREATE INDEX IF NOT EXISTS idx_news_crawl_time ON news_items(last_crawl_time DESC);

-- 标题索引
CREATE INDEX IF NOT EXISTS idx_news_title ON news_items USING gin(to_tsvector('simple', title));

-- URL 唯一索引
CREATE UNIQUE INDEX IF NOT EXISTS idx_news_url_platform
    ON news_items(url, platform_id) WHERE url != '';

-- 排名历史索引
CREATE INDEX IF NOT EXISTS idx_rank_history_news ON rank_history(news_item_id);
CREATE INDEX IF NOT EXISTS idx_rank_history_time ON rank_history(crawl_time DESC);

-- RSS 索引
CREATE INDEX IF NOT EXISTS idx_rss_items_feed ON rss_items(feed_id);
CREATE INDEX IF NOT EXISTS idx_rss_items_published ON rss_items(published_at DESC);

-- ============================================
-- RLS (Row Level Security) 策略
-- ============================================

-- 启用 RLS
ALTER TABLE platforms ENABLE ROW LEVEL SECURITY;
ALTER TABLE news_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE rank_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE rss_feeds ENABLE ROW LEVEL SECURITY;
ALTER TABLE rss_items ENABLE ROW LEVEL SECURITY;

-- 允许匿名读取
CREATE POLICY "Allow anonymous read access" ON platforms FOR SELECT USING (true);
CREATE POLICY "Allow anonymous read access" ON news_items FOR SELECT USING (true);
CREATE POLICY "Allow anonymous read access" ON rank_history FOR SELECT USING (true);
CREATE POLICY "Allow anonymous read access" ON rss_feeds FOR SELECT USING (true);
CREATE POLICY "Allow anonymous read access" ON rss_items FOR SELECT USING (true);

-- ============================================
-- 视图定义
-- ============================================

-- 新闻条目视图 (包含平台名称)
CREATE OR REPLACE VIEW news_items_with_platform AS
SELECT
    n.*,
    p.name as platform_name
FROM news_items n
LEFT JOIN platforms p ON n.platform_id = p.id;

-- RSS 条目视图 (包含订阅源名称)
CREATE OR REPLACE VIEW rss_items_with_feed AS
SELECT
    r.*,
    f.name as feed_name
FROM rss_items r
LEFT JOIN rss_feeds f ON r.feed_id = f.id;
