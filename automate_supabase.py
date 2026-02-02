#!/usr/bin/env python3
"""
自动化脚本：获取 Supabase connection pooling 连接字符串并更新 GitHub Secret
"""
import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        # 启动浏览器（使用用户的 Chrome profile）
        print("🚀 启动浏览器...")
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome"
        )

        context = await browser.new_context()
        page = await context.new_page()

        try:
            # 步骤 1: 先访问 Supabase 主页检查登录状态
            print("\n📊 访问 Supabase...")
            await page.goto("https://supabase.com/dashboard", timeout=60000)
            await asyncio.sleep(3)

            # 检查是否需要登录
            if "sign-in" in page.url or "login" in page.url:
                print("❌ 需要登录 Supabase。")
                print("请在打开的浏览器中登录，然后按回车继续...")
                input()
                await page.goto("https://supabase.com/dashboard", timeout=60000)
                await asyncio.sleep(3)

            # 访问数据库设置页面
            print("\n📊 访问数据库设置页面...")
            supabase_url = "https://supabase.com/dashboard/project/sqnfcrywcddssjopdcde/settings/database"
            await page.goto(supabase_url, timeout=60000)
            await asyncio.sleep(5)

            print("✅ 已进入 Supabase Dashboard")

            # 步骤 2: 查找 Connection Pooling 部分
            print("\n🔍 查找 Connection Pooling 连接字符串...")

            # 尝试点击 "Connection Pooling" 标签
            try:
                # 等待并点击 Connection Pooling 标签
                await page.click('text="Connection pooling"', timeout=5000)
                await asyncio.sleep(2)
                print("✅ 已切换到 Connection Pooling 标签")
            except:
                print("⚠️  未找到 Connection Pooling 标签，尝试其他方法...")

            # 尝试查找包含 6543 端口的连接字符串
            page_content = await page.content()

            # 查找 PostgreSQL 连接字符串（端口 6543）
            pattern = r'postgresql://[^:]+:[^@]+@[^:]+:6543/[^\s<>"\']+'
            matches = re.findall(pattern, page_content)

            if matches:
                connection_string = matches[0]
                # 清理可能的 HTML 实体
                connection_string = connection_string.replace('&quot;', '').replace('&#x27;', '')
                print(f"\n✅ 找到 Connection Pooling 连接字符串:")
                print(f"   {connection_string[:50]}...{connection_string[-20:]}")

                # 确保密码中的 @ 被编码
                if '@' in connection_string.split('@')[0]:
                    # 密码部分包含 @，需要编码
                    parts = connection_string.split('://')
                    if len(parts) == 2:
                        protocol = parts[0]
                        rest = parts[1]
                        # 分离用户名:密码 和 主机部分
                        auth_host = rest.split('@')
                        if len(auth_host) >= 2:
                            auth = auth_host[0]  # username:password
                            host = '@'.join(auth_host[1:])  # host:port/db
                            # 编码密码中的 @
                            if ':' in auth:
                                username, password = auth.split(':', 1)
                                password = password.replace('@', '%40')
                                connection_string = f"{protocol}://{username}:{password}@{host}"
                                print(f"\n✅ 已编码密码中的特殊字符")

                print(f"\n最终连接字符串: {connection_string}")

            else:
                print("❌ 未找到 Connection Pooling 连接字符串")
                print("\n请手动复制连接字符串，然后按回车继续...")
                connection_string = input("请粘贴连接字符串: ").strip()

            # 步骤 3: 访问 GitHub 更新 Secret
            print("\n🔐 访问 GitHub 更新 Secret...")
            github_url = "https://github.com/xiaoanzi123/TrendRadar-Dashboard/settings/secrets/actions"
            await page.goto(github_url, timeout=60000)
            await asyncio.sleep(3)

            # 检查是否需要登录
            if "login" in page.url:
                print("❌ 需要登录 GitHub。请在浏览器中登录后按回车继续...")
                input()
                await page.goto(github_url, timeout=60000)
                await asyncio.sleep(3)

            print("✅ 已进入 GitHub Secrets 页面")

            # 查找 DATABASE_URL secret 并点击更新
            print("\n🔄 更新 DATABASE_URL Secret...")
            try:
                # 查找 DATABASE_URL 行并点击 Update 按钮
                await page.click('text="DATABASE_URL"', timeout=5000)
                await asyncio.sleep(1)

                # 或者直接查找 Update 按钮
                update_buttons = await page.query_selector_all('button:has-text("Update")')
                if update_buttons:
                    await update_buttons[0].click()
                    await asyncio.sleep(2)
                    print("✅ 已打开更新对话框")

                    # 清空并输入新的连接字符串
                    await page.fill('textarea[name="secret_value"]', connection_string)
                    await asyncio.sleep(1)

                    # 点击 Update secret 按钮
                    await page.click('button:has-text("Update secret")')
                    await asyncio.sleep(2)

                    print("✅ DATABASE_URL Secret 已更新！")
                else:
                    print("⚠️  未找到 Update 按钮，请手动更新")
                    print(f"\n请将以下连接字符串复制到 DATABASE_URL Secret:")
                    print(f"{connection_string}")
                    input("\n更新完成后按回车继续...")

            except Exception as e:
                print(f"⚠️  自动更新失败: {e}")
                print(f"\n请手动更新 DATABASE_URL Secret:")
                print(f"{connection_string}")
                input("\n更新完成后按回车继续...")

            print("\n✅ 所有操作完成！")

        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()

        finally:
            print("\n按回车关闭浏览器...")
            input()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
