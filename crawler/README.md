# TrendRadar Crawler

自动化热点数据爬虫，使用 GitHub Actions 定时抓取各大平台热点并存入 Supabase。

## 🚀 功能特性

- ✅ 支持 8+ 主流平台（微博、知乎、抖音、B站、百度等）
- ✅ 每小时自动抓取最新热点
- ✅ 数据自动存入 Supabase 数据库
- ✅ 完全免费（GitHub Actions 免费额度）
- ✅ 无需服务器，全自动运行

## 📋 配置步骤

### 1. 配置 GitHub Secrets

在你的 GitHub 仓库中设置以下 Secret：

1. 进入仓库页面
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 添加以下 Secret：

**DATABASE_URL**
```
postgresql://postgres:CAF@sbb1991328@db.sqnfcrywcddssjopdcde.supabase.co:5432/postgres
```

### 2. 启用 GitHub Actions

1. 进入仓库的 `Actions` 标签页
2. 如果提示启用 Workflows，点击 `I understand my workflows, go ahead and enable them`
3. 找到 `TrendRadar Crawler` workflow
4. 点击 `Enable workflow`

### 3. 手动测试运行

1. 在 `Actions` 页面，选择 `TrendRadar Crawler`
2. 点击 `Run workflow` → `Run workflow`
3. 等待运行完成，查看日志确认是否成功

## ⏰ 运行时间

- **自动运行**: 每小时一次（整点执行）
- **手动运行**: 随时可以在 Actions 页面手动触发

## 📊 数据流程

```
GitHub Actions (每小时)
    ↓
运行 Python 爬虫
    ↓
调用各平台 API
    ↓
存入 Supabase 数据库
    ↓
Dashboard 自动显示最新数据
```

## 🔧 本地测试

如果想在本地测试爬虫：

```bash
# 1. 进入 crawler 目录
cd crawler

# 2. 安装依赖
pip install -r requirements.txt

# 3. 设置环境变量
export DATABASE_URL="postgresql://..."

# 4. 运行爬虫
python crawler.py
```

## 📝 注意事项

- GitHub Actions 免费额度：每月 2000 分钟
- 每次运行约 1-2 分钟
- 每小时运行一次，每月约 720 次，完全够用
- 如果需要更频繁的更新，可以修改 `.github/workflows/crawler.yml` 中的 cron 表达式

## 🎯 支持的平台

- 微博热搜
- 知乎热榜
- 抖音热榜
- B站热门
- 百度热搜
- 今日头条
- 36氪
- 少数派

## �� 修改抓取频率

编辑 `.github/workflows/crawler.yml`：

```yaml
schedule:
  - cron: '0 * * * *'  # 每小时
  # - cron: '*/30 * * * *'  # 每30分钟
  # - cron: '0 */2 * * *'  # 每2小时
```

## 📞 问题排查

如果爬虫运行失败：

1. 检查 Actions 日志查看错误信息
2. 确认 DATABASE_URL Secret 配置正确
3. 确认 Supabase 数据库可以访问
4. 检查数据库表结构是否正确

## 📄 License

MIT
