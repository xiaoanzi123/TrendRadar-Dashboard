#!/usr/bin/env python3
"""
简化版自动化脚本：打开 Supabase 页面并截图
"""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("🚀 启动浏览器...")
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome"
        )

        context = await browser.new_context()
        page = await context.new_page()

        try:
            # 访问 Supabase 数据库设置页面
            print("\n📊 访问 Supabase Dashboard...")
            await page.goto("https://supabase.com/dashboard", timeout=60000)
            await asyncio.sleep(3)

            print("✅ 已打开 Supabase Dashboard")
            print("\n请在浏览器中：")
            print("1. 导航到你的项目")
            print("2. 点击左侧 Settings → Database")
            print("3. 找到 'Connection string' 部分")
            print("4. 点击 'Connection pooling' 标签")
            print("5. 复制 URI 格式的连接字符串")

            # 等待用户操作
            await asyncio.sleep(60)

            # 截图
            print("\n📸 正在截图...")
            await page.screenshot(path="supabase_screenshot.png", full_page=True)
            print("✅ 截图已保存到 supabase_screenshot.png")

        except Exception as e:
            print(f"\n❌ 发生错误: {e}")

        finally:
            await browser.close()
            print("\n✅ 浏览器已关闭")

if __name__ == "__main__":
    asyncio.run(main())
