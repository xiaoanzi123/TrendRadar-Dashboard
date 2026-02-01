import { useLatestNews, usePlatformStats, useTrendData } from '@/hooks/useData'
import ReactECharts from 'echarts-for-react'
import { formatRelativeTime, getPlatformColor } from '@/lib/utils'
import type { NewsItem, PlatformStat, TrendData } from '@/types'

export default function Dashboard() {
  const { data: latestNews, isLoading: newsLoading } = useLatestNews(30)
  const { data: platformStats, isLoading: statsLoading } = usePlatformStats()
  const { data: trendData, isLoading: trendLoading } = useTrendData(7)

  // 平台分布饼图配置
  const platformChartOption = {
    title: { text: '平台热点分布', left: 'center' },
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [
      {
        name: '热点数量',
        type: 'pie',
        radius: '50%',
        data: platformStats?.map((stat: PlatformStat) => ({
          value: stat.total_items,
          name: stat.platform_name,
          itemStyle: { color: getPlatformColor(stat.platform_id) },
        })) || [],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  }

  // 趋势折线图配置
  const trendChartOption = {
    title: { text: '热点趋势 (最近7天)', left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: trendData?.map((d: TrendData) => d.date) || [],
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '热点数量',
        type: 'line',
        data: trendData?.map((d: TrendData) => d.count) || [],
        smooth: true,
        areaStyle: { opacity: 0.3 },
      },
    ],
  }

  if (newsLoading || statsLoading || trendLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">加载中...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-500">总热点数</div>
          <div className="text-3xl font-bold text-gray-900 mt-2">
            {latestNews?.length || 0}
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-500">活跃平台</div>
          <div className="text-3xl font-bold text-gray-900 mt-2">
            {platformStats?.length || 0}
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-500">今日更新</div>
          <div className="text-3xl font-bold text-gray-900 mt-2">
            {trendData?.[trendData.length - 1]?.count || 0}
          </div>
        </div>
      </div>

      {/* 图表 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <ReactECharts option={platformChartOption} style={{ height: '400px' }} />
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <ReactECharts option={trendChartOption} style={{ height: '400px' }} />
        </div>
      </div>

      {/* 最新热点列表 */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-semibold text-gray-900">最新热点</h2>
        </div>
        <div className="divide-y">
          {latestNews?.map((item: NewsItem) => (
            <div key={item.id} className="px-6 py-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {item.platform_name || item.platform_id}
                    </span>
                    <span className="text-sm text-gray-500">
                      #{item.rank}
                    </span>
                  </div>
                  <h3 className="mt-2 text-base font-medium text-gray-900">
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
                    {formatRelativeTime(item.last_crawl_time)} · 抓取 {item.crawl_count} 次
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
