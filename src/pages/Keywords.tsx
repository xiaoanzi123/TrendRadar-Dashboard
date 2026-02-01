import { useKeywordStats } from '@/hooks/useData'
import ReactECharts from 'echarts-for-react'
import type { KeywordStat } from '@/types'

export default function Keywords() {
  const { data: keywordStats, isLoading } = useKeywordStats()

  // 关键词云图配置
  const wordCloudOption = {
    title: { text: '热门关键词', left: 'center' },
    tooltip: { trigger: 'item' },
    series: [
      {
        type: 'wordCloud',
        shape: 'circle',
        sizeRange: [12, 60],
        rotationRange: [0, 0],
        data: keywordStats?.slice(0, 50).map((stat: KeywordStat) => ({
          name: stat.keyword,
          value: stat.count,
        })) || [],
      },
    ],
  }

  // 关键词柱状图配置
  const barChartOption = {
    title: { text: 'Top 20 关键词', left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'value',
    },
    yAxis: {
      type: 'category',
      data: keywordStats?.slice(0, 20).map((stat: KeywordStat) => stat.keyword).reverse() || [],
    },
    series: [
      {
        name: '出现次数',
        type: 'bar',
        data: keywordStats?.slice(0, 20).map((stat: KeywordStat) => stat.count).reverse() || [],
        itemStyle: {
          color: '#5470c6',
        },
      },
    ],
  }

  if (isLoading) {
    return <div className="text-center py-8">加载中...</div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">关键词分析</h1>
        <p className="mt-1 text-sm text-gray-500">
          热门关键词统计与分析
        </p>
      </div>

      {/* 图表 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <ReactECharts option={wordCloudOption} style={{ height: '500px' }} />
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <ReactECharts option={barChartOption} style={{ height: '500px' }} />
        </div>
      </div>

      {/* 关键词列表 */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-semibold text-gray-900">关键词详情</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  排名
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  关键词
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  出现次数
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  相关平台
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {keywordStats?.slice(0, 50).map((stat: KeywordStat, index: number) => (
                <tr key={stat.keyword} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    #{index + 1}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {stat.keyword}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {stat.count}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    <div className="flex flex-wrap gap-1">
                      {stat.platforms?.slice(0, 5).map((platform: string) => (
                        <span
                          key={platform}
                          className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                        >
                          {platform}
                        </span>
                      ))}
                      {stat.platforms?.length > 5 && (
                        <span className="text-xs text-gray-400">
                          +{stat.platforms.length - 5}
                        </span>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
