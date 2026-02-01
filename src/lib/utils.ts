import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { format, formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date, formatStr = 'yyyy-MM-dd HH:mm:ss') {
  return format(new Date(date), formatStr, { locale: zhCN })
}

export function formatRelativeTime(date: string | Date) {
  return formatDistanceToNow(new Date(date), { addSuffix: true, locale: zhCN })
}

export function truncateText(text: string, maxLength: number) {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

export function getColorByIndex(index: number) {
  const colors = [
    '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
    '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#5470c6'
  ]
  return colors[index % colors.length]
}

export function getPlatformColor(platformId: string) {
  const colors: Record<string, string> = {
    'weibo': '#e6162d',
    'zhihu': '#0084ff',
    'douyin': '#000000',
    'bilibili-hot-search': '#00a1d6',
    'baidu': '#2932e1',
    'toutiao': '#d32f2f',
    'wallstreetcn-hot': '#1976d2',
    'cls-hot': '#c62828',
  }
  return colors[platformId] || getColorByIndex(platformId.charCodeAt(0))
}
