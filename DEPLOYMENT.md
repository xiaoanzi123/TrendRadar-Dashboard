# TrendRadar Dashboard 部署指南

## 📋 目录
- [快速开始](#快速开始)
- [Supabase 配置](#supabase-配置)
- [Vercel 部署](#vercel-部署)
- [本地开发](#本地开发)
- [数据迁移](#数据迁移)

---

## 🚀 快速开始

### 前置要求
- Node.js 18+
- npm 或 yarn
- Supabase 账号 (免费)
- Vercel 账号 (免费)

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd TrendRadar-Dashboard
```

### 2. 安装依赖
```bash
npm install
```

### 3. 配置环境变量
```bash
cp .env.example .env.local
```

编辑 `.env.local` 填入配置：
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

---

## 🗄️ Supabase 配置

### 1. 创建 Supabase 项目

1. 访问 [Supabase](https://supabase.com)
2. 点击 "New Project"
3. 填写项目信息并创建

### 2. 运行数据库迁移

在 Supabase Dashboard 中：

1. 进入 **SQL Editor**
2. 复制 `supabase/schema.sql` 的内容
3. 粘贴并执行

### 3. 获取 API 密钥

在 Supabase Dashboard 中：

1. 进入 **Settings** → **API**
2. 复制以下信息：
   - Project URL → `VITE_SUPABASE_URL`
   - anon public key → `VITE_SUPABASE_ANON_KEY`

### 4. 配置 RLS (Row Level Security)

数据库已自动配置 RLS 策略，允许匿名读取。如需修改权限，在 SQL Editor 中执行：

```sql
-- 示例：允许认证用户写入
CREATE POLICY "Allow authenticated write"
ON news_items FOR INSERT
TO authenticated
WITH CHECK (true);
```

---

## 🌐 Vercel 部署

### 方法 1: 通过 Vercel CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
vercel
```

### 方法 2: 通过 GitHub 集成

1. 将代码推送到 GitHub
2. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
3. 点击 "Import Project"
4. 选择你的 GitHub 仓库
5. 配置环境变量：
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
6. 点击 "Deploy"

### 环境变量配置

在 Vercel Dashboard 中：

1. 进入项目 → **Settings** → **Environment Variables**
2. 添加以下变量：
   ```
   VITE_SUPABASE_URL = https://your-project.supabase.co
   VITE_SUPABASE_ANON_KEY = your-anon-key
   ```
3. 重新部署

---

## 💻 本地开发

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

---

## 📊 数据迁移

### 从 TrendRadar SQLite 迁移到 Supabase

#### 方法 1: 使用 Python 脚本

创建 `migrate.py`:

```python
import sqlite3
import psycopg2
from datetime import datetime

# SQLite 连接
sqlite_conn = sqlite3.connect('output/news/2025-01-27.db')
sqlite_cursor = sqlite_conn.cursor()

# PostgreSQL 连接
pg_conn = psycopg2.connect(
    host="db.your-project.supabase.co",
    database="postgres",
    user="postgres",
    password="your-password"
)
pg_cursor = pg_conn.cursor()

# 迁移平台数据
sqlite_cursor.execute("SELECT * FROM platforms")
platforms = sqlite_cursor.fetchall()

for platform in platforms:
    pg_cursor.execute(
        "INSERT INTO platforms (id, name, is_active, updated_at) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
        platform
    )

# 迁移新闻数据
sqlite_cursor.execute("SELECT * FROM news_items")
news_items = sqlite_cursor.fetchall()

for item in news_items:
    pg_cursor.execute(
        """INSERT INTO news_items
        (title, platform_id, rank, url, mobile_url, first_crawl_time, last_crawl_time, crawl_count, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        item[1:]  # 跳过 id，使用自动生成
    )

pg_conn.commit()
print("迁移完成！")
```

运行迁移：
```bash
pip install psycopg2-binary
python migrate.py
```

#### 方法 2: 使用 Supabase CLI

```bash
# 安装 Supabase CLI
npm install -g supabase

# 导出 SQLite 数据为 CSV
sqlite3 output/news/2025-01-27.db <<EOF
.headers on
.mode csv
.output platforms.csv
SELECT * FROM platforms;
.output news_items.csv
SELECT * FROM news_items;
EOF

# 使用 Supabase Dashboard 导入 CSV
# 进入 Table Editor → Import Data
```

---

## 🔧 故障排除

### 问题 1: CORS 错误

确保 Vercel Serverless Functions 已设置 CORS 头：
```python
self.send_header('Access-Control-Allow-Origin', '*')
```

### 问题 2: Supabase 连接���败

检查：
1. URL 和 API Key 是否正确
2. RLS 策略是否配置
3. 网络连接是否正常

### 问题 3: 构建失败

清除缓存并重新安装：
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 📚 API 文档

### Supabase 直接查询

```typescript
// 获取平台列表
const { data } = await supabase
  .from('platforms')
  .select('*')
  .eq('is_active', true)

// 获取最新新闻
const { data } = await supabase
  .from('news_items')
  .select('*, platforms(name)')
  .order('last_crawl_time', { ascending: false })
  .limit(50)
```

### Serverless Functions

```bash
# 获取平台统计
GET /api/stats/platforms?date=2025-01-27

# 获取关键词统计
GET /api/stats/keywords

# 获取趋势数据
GET /api/stats/trends?days=7

# 获取 RSS 订阅源
GET /api/rss/feeds

# 获取 RSS 条目
GET /api/rss/items?feed_id=hacker-news&limit=50
```

---

## 🎯 性能优化

### 1. 启用 Supabase 缓存

```typescript
const { data } = await supabase
  .from('news_items')
  .select('*')
  .limit(50)
  // 缓存 5 分钟
  .abortSignal(AbortSignal.timeout(5000))
```

### 2. 使用 React Query 缓存

已在 `src/main.tsx` 中配置：
```typescript
staleTime: 5 * 60 * 1000, // 5 分钟
```

### 3. 优化图片和资源

```bash
# 压缩构建产物
npm run build
```

---

## 🔐 安全建议

1. **不要提交 `.env.local`** - 已在 `.gitignore` 中
2. **使用 Supabase RLS** - 限制数据访问权限
3. **定期更新依赖** - `npm audit fix`
4. **使用 HTTPS** - Vercel 自动提供

---

## 📞 支持

遇到问题？

1. 查看 [Issues](https://github.com/your-repo/issues)
2. 阅读 [Supabase 文档](https://supabase.com/docs)
3. 阅读 [Vercel 文档](https://vercel.com/docs)

---

## 📄 License

GPL-3.0 (继承自 TrendRadar)
