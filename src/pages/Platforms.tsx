import { useState } from 'react'
import { usePlatforms, useNewsByPlatform } from '@/hooks/useData'
import { formatRelativeTime } from '@/lib/utils'
import type { Platform, NewsItem } from '@/types'

export default function Platforms() {
  const { data: platforms, isLoading } = usePlatforms()
  const [selectedPlatform, setSelectedPlatform] = useState<string>('')

  const { data: platformNews } = useNewsByPlatform(selectedPlatform)

  if (isLoading) {
    return <div className="text-center py-8">加载中...</div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">平台管理</h1>
        <p className="mt-1 text-sm text-gray-500">
          查看各平台的热点数据
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 平台列表 */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-semibold text-gray-900">平台列表</h2>
          </div>
          <div className="divide-y max-h-[600px] overflow-y-auto">
            {platforms?.map((platform: Platform) => (
              <button
                key={platform.id}
                onClick={() => setSelectedPlatform(platform.id)}
                className={`w-full px-6 py-4 text-left hover:bg-gray-50 transition-colors ${
                  selectedPlatform === platform.id ? 'bg-blue-50' : ''
                }`}
              >
                <div className="font-medium text-gray-900">{platform.name}</div>
                <div className="text-sm text-gray-500">{platform.id}</div>
              </button>
            ))}
          </div>
        </div>

        {/* 平台详情 */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-semibold text-gray-900">
              {selectedPlatform
                ? platforms?.find((p: Platform) => p.id === selectedPlatform)?.name
                : '选择平台查看详情'}
            </h2>
          </div>
          <div className="divide-y max-h-[600px] overflow-y-auto">
            {platformNews?.length ? (
              platformNews.map((item: NewsItem) => (
                <div key={item.id} className="px-6 py-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-gray-500">
                          #{item.rank}
                        </span>
                      </div>
                      <h3 className="mt-1 text-base font-medium text-gray-900">
                        {item.url ? (
                          <a
                            href={item.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hover:text-blue-600"
                          >
                            {item.title}
                          </a>
                        ) : (
                          item.title
                        )}
                      </h3>
                      <div className="mt-1 text-sm text-gray-500">
                        {formatRelativeTime(item.last_crawl_time)}
                      </div>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="px-6 py-8 text-center text-gray-500">
                {selectedPlatform ? '暂无数据' : '请选择平台'}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
