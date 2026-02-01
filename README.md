# TrendRadar Dashboard

基于 TrendRadar 的可视化 Dashboard，采用现代化技术栈。

## 技术栈

### 前端
- React 18 + TypeScript
- Vite (构建工具)
- TanStack Query (数据获取)
- ECharts (数据可视化)
- Tailwind CSS + shadcn/ui

### 后端
- Vercel Serverless Functions
- Supabase (PostgreSQL 数据库)

### 部署
- 前端: Vercel
- 数据库: Supabase
- 完全免费方案

## 快速开始

### 1. 安装依赖
```bash
npm install
```

### 2. 配置环境变量
```bash
cp .env.example .env.local
# 编辑 .env.local 填入 Supabase 配置
```

### 3. 启动开发服务器
```bash
npm run dev
```

### 4. 部署到 Vercel
```bash
npm run deploy
```

## 功能特性

- ✅ 实时热点监控
- ✅ 多平台数据对比
- ✅ 关键词热度分析
- ✅ 历史趋势图表
- ✅ RSS 订阅管理
- ✅ AI 分析结果展示
- ✅ 响应式设计

## 目录结构

```
.
├── src/
│   ├── components/     # React 组件
│   ├── pages/          # 页面
│   ├── api/            # API 客户端
│   ├── hooks/          # 自定义 Hooks
│   ├── lib/            # 工具函数
│   └── types/          # TypeScript 类型
├── api/                # Vercel Serverless Functions
├── public/             # 静态资源
└── supabase/           # 数据库迁移脚本
```

## License

GPL-3.0 (继承自 TrendRadar)
