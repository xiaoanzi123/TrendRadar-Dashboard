import { useRSSFeeds, useRSSItems } from '@/hooks/useData'
import { formatRelativeTime } from '@/lib/utils'
import { useState } from 'react'
import type { RSSFeed, RSSItem } from '@/types'

export default function RSS() {
  const { data: feeds, isLoading: feedsLoading } = useRSSFeeds()
  const [selectedFeed, setSelectedFeed] = useState<string>('')
  const { data: items, isLoading: itemsLoading } = useRSSItems(selectedFeed)

  if (feedsLoading) {
    return <div className="text-center py-8">加载中...</div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">RSS 订阅</h1>
        <p className="mt-1 text-sm text-gray-500">
          管理和查看 RSS 订阅源
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* RSS 源列表 */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-semibold text-gray-900">订阅源</h2>
          </div>
          <div className="divide-y max-h-[600px] overflow-y-auto">
            <button
              onClick={() => setSelectedFeed('')}
              className={`w-full px-6 py-4 text-left hover:bg-gray-50 transition-colors ${
                !selectedFeed ? 'bg-blue-50' : ''
              }`}
            >
              <div className="font-medium text-gray-900">全部</div>
              <div className="text-sm text-gray-500">查看所有订阅</div>
            </button>
            {feeds?.map((feed: RSSFeed) => (
              <button
                key={feed.id}
                onClick={() => setSelectedFeed(feed.id)}
                className={`w-full px-6 py-4 text-left hover:bg-gray-50 transition-colors ${
                  selectedFeed === feed.id ? 'bg-blue-50' : ''
                }`}
              >
                <div className="font-medium text-gray-900">{feed.name}</div>
                <div className="text-sm text-gray-500 truncate">{feed.url}</div>
              </button>
            ))}
          </div>
        </div>

        {/* RSS 内容 */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-semibold text-gray-900">
              {selectedFeed
                ? feeds?.find((f: RSSFeed) => f.id === selectedFeed)?.name
                : '全部订阅'}
            </h2>
          </div>
          <div className="divide-y max-h-[600px] overflow-y-auto">
            {itemsLoading ? (
              <div className="px-6 py-8 text-center text-gray-500">加载中...</div>
            ) : items?.length ? (
              items.map((item: RSSItem) => (
                <div key={item.id} className="px-6 py-4 hover:bg-gray-50">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {item.feed_name || item.feed_id}
                        </span>
                      </div>
                      <h3 className="mt-2 text-base font-medium text-gray-900">
                        <a
                          href={item.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="hover:text-blue-600"
                        >
                          {item.title}
                        </a>
                      </h3>
                      {item.summary && (
                        <p className="mt-1 text-sm text-gray-600 line-clamp-2">
                          {item.summary}
                        </p>
                      )}
                      <div className="mt-1 text-sm text-gray-500">
                        {formatRelativeTime(item.published_at)}
                      </div>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="px-6 py-8 text-center text-gray-500">
                暂无数据
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
