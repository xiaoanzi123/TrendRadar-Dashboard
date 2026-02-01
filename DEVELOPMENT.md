# TrendRadar Dashboard 开发指南

## 项目结构

```
TrendRadar-Dashboard/
├── src/
│   ├── components/      # React 组件
│   │   └── Layout.tsx   # 布局组件
│   ├── pages/           # 页面组件
│   │   ├── Dashboard.tsx    # 概览页
│   │   ├── Platforms.tsx    # 平台页
│   │   ├── Keywords.tsx     # 关键词页
│   │   ├── History.tsx      # 历史页
│   │   ├── RSS.tsx          # RSS 页
│   │   └── Settings.tsx     # 设置页
│   ├── hooks/           # 自定义 Hooks
│   │   └── useData.ts   # 数据获取 Hooks
│   ├── lib/             # 工具函数
│   │   ├── api.ts       # API 客户端
│   │   └── utils.ts     # 通用工具
│   ├── types/           # TypeScript 类型
│   │   └── index.ts     # 类型定义
│   ├── App.tsx          # 应用入口
│   ├── main.tsx         # React 入口
│   └── index.css        # 全局样式
├── api/                 # Vercel Serverless Functions
│   ├── stats.py         # 统计 API
│   └── rss.py           # RSS API
├── supabase/            # 数据库脚本
│   └── schema.sql       # 数据库架构
├── scripts/             # 部署脚本
│   ├── migrate_to_supabase.py  # 数据迁移
│   └── deploy.sh        # 部署脚本
├── public/              # 静态资源
├── package.json         # 项目配置
├── vite.config.ts       # Vite 配置
├── tailwind.config.js   # Tailwind 配置
├── tsconfig.json        # TypeScript 配置
├── vercel.json          # Vercel 配置
├── README.md            # 项目说明
└── DEPLOYMENT.md        # 部署指南
```

## 技术栈详解

### 前端

- **React 18**: UI 框架
- **TypeScript**: 类型安全
- **Vite**: 快速构建工具
- **TanStack Query**: 数据获取和缓存
- **React Router**: 路由管理
- **ECharts**: 数据可视化
- **Tailwind CSS**: 样式框架

### 后端

- **Vercel Serverless Functions**: 无服务器 API
- **Supabase**: PostgreSQL 数据库 + 实时订阅
- **Python**: API 实现语言

### 部署

- **Vercel**: 前端托管 + Serverless Functions
- **Supabase**: 数据库托管
- **GitHub**: 代码托管 + CI/CD

## 开发工作流

### 1. 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:3000
```

### 2. 添加新页面

1. 在 `src/pages/` 创建新组件
2. 在 `src/App.tsx` 添加路由
3. 在 `src/components/Layout.tsx` 添加导航

示例:
```typescript
// src/pages/NewPage.tsx
export default function NewPage() {
  return <div>New Page</div>
}

// src/App.tsx
import NewPage from './pages/NewPage'

<Route path="/new" element={<NewPage />} />
```

### 3. 添加新 API

1. 在 `api/` 创建新的 Python 文件
2. 实现 `handler` 类
3. 在 `src/lib/api.ts` 添加客户端方法

示例:
```python
# api/new.py
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        response = {'data': 'Hello'}
        self.wfile.write(json.dumps(response).encode())
```

```typescript
// src/lib/api.ts
async getNewData() {
  const response = await fetch(`${API_BASE_URL}/new`)
  return response.json()
}
```

### 4. 数据库操作

使用 Supabase 客户端:

```typescript
import { supabase } from '@/lib/api'

// 查询
const { data, error } = await supabase
  .from('table_name')
  .select('*')
  .eq('column', 'value')

// 插入
const { data, error } = await supabase
  .from('table_name')
  .insert({ column: 'value' })

// 更新
const { data, error } = await supabase
  .from('table_name')
  .update({ column: 'new_value' })
  .eq('id', 1)

// 删除
const { data, error } = await supabase
  .from('table_name')
  .delete()
  .eq('id', 1)
```

### 5. 实时订阅

```typescript
// 订阅表变化
const subscription = supabase
  .channel('table_changes')
  .on('postgres_changes', {
    event: '*',
    schema: 'public',
    table: 'news_items'
  }, (payload) => {
    console.log('Change received!', payload)
  })
  .subscribe()

// 取消订阅
subscription.unsubscribe()
```

## 常见任务

### 添加新的数据可视化

```typescript
import ReactECharts from 'echarts-for-react'

const option = {
  title: { text: '图表标题' },
  xAxis: { type: 'category', data: ['A', 'B', 'C'] },
  yAxis: { type: 'value' },
  series: [{
    data: [120, 200, 150],
    type: 'bar'
  }]
}

<ReactECharts option={option} style={{ height: '400px' }} />
```

### 添加新的 Hook

```typescript
// src/hooks/useCustomData.ts
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function useCustomData() {
  return useQuery({
    queryKey: ['custom'],
    queryFn: api.getCustomData,
    refetchInterval: 60000, // 每分钟刷新
  })
}
```

### 样式定制

使用 Tailwind CSS:

```tsx
<div className="bg-white rounded-lg shadow p-6">
  <h2 className="text-lg font-semibold text-gray-900">标题</h2>
  <p className="mt-2 text-sm text-gray-500">内容</p>
</div>
```

## 性能优化

### 1. 代码分割

```typescript
// 懒加载页面
const Dashboard = lazy(() => import('./pages/Dashboard'))

<Suspense fallback={<div>Loading...</div>}>
  <Dashboard />
</Suspense>
```

### 2. 图片优化

```bash
# 使用 WebP 格式
# 压缩图片
```

### 3. 缓存策略

```typescript
// React Query 缓存配置
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 分钟
      cacheTime: 10 * 60 * 1000, // 10 分钟
    },
  },
})
```

## 调试技巧

### 1. React DevTools

安装浏览器扩展: React Developer Tools

### 2. 查看网络请求

```typescript
// 在 api.ts 中添加日志
console.log('API Request:', url)
console.log('API Response:', data)
```

### 3. Supabase 日志

在 Supabase Dashboard → Logs 查看数据库查询日志

## 测试

### 单元测试 (TODO)

```bash
npm install -D vitest @testing-library/react
```

### E2E 测试 (TODO)

```bash
npm install -D playwright
```

## 贡献指南

1. Fork 项目
2. 创建特性分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -m 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 提交 Pull Request

## License

GPL-3.0
