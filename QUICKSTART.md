# 🚀 TrendRadar Dashboard 快速开始

## 5 分钟部署指南

### 步骤 1: 创建 Supabase 项目 (2 分钟)

1. 访问 https://supabase.com 并登录
2. 点击 "New Project"
3. 填写项目信息并等待创建完成
4. 进入 **SQL Editor**，复制粘贴 `supabase/schema.sql` 的内容并执行
5. 进入 **Settings** → **API**，复制：
   - Project URL
   - anon public key

### 步骤 2: 部署到 Vercel (2 分钟)

#### 方法 A: 通过 GitHub (推荐)

1. 将代码推送到 GitHub
2. 访问 https://vercel.com 并登录
3. 点击 "Import Project"
4. 选择你的 GitHub 仓库
5. 添加环境变量：
   ```
   VITE_SUPABASE_URL = 你的 Supabase URL
   VITE_SUPABASE_ANON_KEY = 你的 Supabase Key
   ```
6. 点击 "Deploy"

#### 方法 B: 通过 CLI

```bash
# ���装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
vercel

# 添加环境变量
vercel env add VITE_SUPABASE_URL
vercel env add VITE_SUPABASE_ANON_KEY

# 重新部署
vercel --prod
```

### 步骤 3: 迁移数据 (1 分钟)

```bash
# 安装依赖
pip install psycopg2-binary

# 运行迁移脚本
python scripts/migrate_to_supabase.py \
  --sqlite-db /path/to/trendradar/output/news/2025-01-27.db \
  --supabase-url https://your-project.supabase.co \
  --supabase-key your-service-key
```

### 完成！

访问你的 Vercel 部署 URL，例如：
```
https://trendradar-dashboard.vercel.app
```

---

## 本地开发

```bash
# 1. 克隆项目
git clone <your-repo>
cd TrendRadar-Dashboard

# 2. 安装依赖
npm install

# 3. 配置环境变量
cp .env.example .env.local
# 编辑 .env.local 填入 Supabase 配置

# 4. 启动开发服务器
npm run dev

# 5. 访问 http://localhost:3000
```

---

## 常见问题

### Q: 如何更新数据？

A: 运行迁移脚本即可增量更新：
```bash
python scripts/migrate_to_supabase.py --sqlite-db latest.db ...
```

### Q: 如何自定义样式？

A: 编辑 `src/index.css` 或使用 Tailwind CSS 类名

### Q: 如何添加新平台？

A: 数据会自动从 TrendRadar 同步，无需手动配置

### Q: 部署失败怎么办？

A: 检查：
1. 环境变量是否正确
2. Supabase 数据库是否已创建表
3. 查看 Vercel 部署日志

---

## 下一步

- 📖 阅读 [DEPLOYMENT.md](DEPLOYMENT.md) 了解详细部署说明
- 💻 阅读 [DEVELOPMENT.md](DEVELOPMENT.md) 了解开发指南
- 🐛 遇到问题？查看 [Issues](https://github.com/your-repo/issues)

---

## 技术支持

- Supabase 文档: https://supabase.com/docs
- Vercel 文档: https://vercel.com/docs
- React 文档: https://react.dev

---

**祝你使用愉快！** 🎉
