import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function usePlatforms() {
  return useQuery({
    queryKey: ['platforms'],
    queryFn: api.getPlatforms,
  })
}

export function useLatestNews(limit = 50) {
  return useQuery({
    queryKey: ['news', 'latest', limit],
    queryFn: () => api.getLatestNews(limit),
    refetchInterval: 60000, // 每分钟刷新
  })
}

export function useNewsByPlatform(platformId: string, limit = 20) {
  return useQuery({
    queryKey: ['news', 'platform', platformId, limit],
    queryFn: () => api.getNewsByPlatform(platformId, limit),
    enabled: !!platformId,
  })
}

export function usePlatformStats(date?: string) {
  return useQuery({
    queryKey: ['stats', 'platforms', date],
    queryFn: () => api.getPlatformStats(date),
  })
}

export function useKeywordStats(date?: string) {
  return useQuery({
    queryKey: ['stats', 'keywords', date],
    queryFn: () => api.getKeywordStats(date),
  })
}

export function useTrendData(days = 7) {
  return useQuery({
    queryKey: ['stats', 'trends', days],
    queryFn: () => api.getTrendData(days),
  })
}

export function useRSSFeeds() {
  return useQuery({
    queryKey: ['rss', 'feeds'],
    queryFn: api.getRSSFeeds,
  })
}

export function useRSSItems(feedId?: string, limit = 50) {
  return useQuery({
    queryKey: ['rss', 'items', feedId, limit],
    queryFn: () => api.getRSSItems(feedId, limit),
    refetchInterval: 300000, // 每5分钟刷新
  })
}
