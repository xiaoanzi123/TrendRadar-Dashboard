export interface Platform {
  id: string
  name: string
  is_active: boolean
  updated_at: string
}

export interface NewsItem {
  id: number
  title: string
  platform_id: string
  platform_name?: string
  rank: number
  url: string
  mobile_url: string
  first_crawl_time: string
  last_crawl_time: string
  crawl_count: number
  created_at: string
  updated_at: string
}

export interface RankHistory {
  id: number
  news_item_id: number
  rank: number
  crawl_time: string
  created_at: string
}

export interface KeywordStat {
  keyword: string
  count: number
  platforms: string[]
  news_items: NewsItem[]
}

export interface PlatformStat {
  platform_id: string
  platform_name: string
  total_items: number
  avg_rank: number
  top_keywords: string[]
}

export interface TrendData {
  date: string
  count: number
  platforms: Record<string, number>
}

export interface RSSFeed {
  id: string
  name: string
  url: string
  enabled: boolean
  max_age_days?: number
}

export interface RSSItem {
  id: number
  feed_id: string
  feed_name?: string
  title: string
  link: string
  published_at: string
  summary?: string
  created_at: string
}
