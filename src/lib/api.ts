import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || ''
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || ''

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// API 客户端
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export const api = {
  // 平台相关
  async getPlatforms() {
    const { data, error } = await supabase
      .from('platforms')
      .select('*')
      .eq('is_active', true)
      .order('name')

    if (error) throw error
    return data
  },

  // 新闻相关
  async getLatestNews(limit = 50) {
    const { data, error } = await supabase
      .from('news_items')
      .select(`
        *,
        platforms (id, name)
      `)
      .order('last_crawl_time', { ascending: false })
      .limit(limit)

    if (error) throw error
    return data
  },

  async getNewsByPlatform(platformId: string, limit = 20) {
    const { data, error } = await supabase
      .from('news_items')
      .select('*')
      .eq('platform_id', platformId)
      .order('rank')
      .limit(limit)

    if (error) throw error
    return data
  },

  async getNewsByDateRange(startDate: string, endDate: string) {
    const { data, error } = await supabase
      .from('news_items')
      .select(`
        *,
        platforms (id, name)
      `)
      .gte('last_crawl_time', startDate)
      .lte('last_crawl_time', endDate)
      .order('last_crawl_time', { ascending: false })

    if (error) throw error
    return data
  },

  // 排名历史
  async getRankHistory(newsItemId: number) {
    const { data, error } = await supabase
      .from('rank_history')
      .select('*')
      .eq('news_item_id', newsItemId)
      .order('crawl_time')

    if (error) throw error
    return data
  },

  // 统计分析
  async getPlatformStats(date?: string) {
    const response = await fetch(`${API_BASE_URL}/stats/platforms${date ? `?date=${date}` : ''}`)
    if (!response.ok) throw new Error('Failed to fetch platform stats')
    return response.json()
  },

  async getKeywordStats(date?: string) {
    const response = await fetch(`${API_BASE_URL}/stats/keywords${date ? `?date=${date}` : ''}`)
    if (!response.ok) throw new Error('Failed to fetch keyword stats')
    return response.json()
  },

  async getTrendData(days = 7) {
    const response = await fetch(`${API_BASE_URL}/stats/trends?days=${days}`)
    if (!response.ok) throw new Error('Failed to fetch trend data')
    return response.json()
  },

  // RSS 相关
  async getRSSFeeds() {
    const response = await fetch(`${API_BASE_URL}/rss/feeds`)
    if (!response.ok) throw new Error('Failed to fetch RSS feeds')
    return response.json()
  },

  async getRSSItems(feedId?: string, limit = 50) {
    const url = feedId
      ? `${API_BASE_URL}/rss/items?feed_id=${feedId}&limit=${limit}`
      : `${API_BASE_URL}/rss/items?limit=${limit}`

    const response = await fetch(url)
    if (!response.ok) throw new Error('Failed to fetch RSS items')
    return response.json()
  },
}
