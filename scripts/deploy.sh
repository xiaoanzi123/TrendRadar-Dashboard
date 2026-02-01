#!/bin/bash
# TrendRadar Dashboard 快速部署脚本

set -e

echo "================================"
echo "TrendRadar Dashboard 部署脚本"
echo "================================"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未安装 Node.js，请先安装: https://nodejs.org/"
    exit 1
fi

echo "✓ Node.js 版本: $(node -v)"

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 未安装 npm"
    exit 1
fi

echo "✓ npm 版本: $(npm -v)"

# 安装依赖
echo ""
echo "📦 安装依赖..."
npm install

# 检查环境变量
if [ ! -f .env.local ]; then
    echo ""
    echo "⚠️  未找到 .env.local 文件"
    echo "正在创建 .env.local..."
    cp .env.example .env.local
    echo ""
    echo "请编辑 .env.local 文件，填入 Supabase 配置："
    echo "  VITE_SUPABASE_URL=https://your-project.supabase.co"
    echo "  VITE_SUPABASE_ANON_KEY=your-anon-key"
    echo ""
    read -p "配置完成后按回车继续..."
fi

# 构建项目
echo ""
echo "🔨 构建项目..."
npm run build

echo ""
echo "================================"
echo "✓ 构建完成！"
echo "================================"
echo ""
echo "下一步："
echo "1. 本地预览: npm run preview"
echo "2. 部署到 Vercel: vercel"
echo ""
