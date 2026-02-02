#!/usr/bin/env python3
"""
自动化脚本：使用 Playwright 获取 Supabase connection pooling 连接字符串
"""
import asyncio
from playwright.async_api import async_playwright
import re
import subprocess

async def main():
    connection_string = None

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
            supabase_url = "https://supabase.com/dashboard/project/sqnfcrywcddssjopdcde/settings/database"
            await page.goto(supabase_url, timeout=60000)

            print("⏳ 等待页面加载...")
            await asyncio.sleep(8)

            # 截图以便调试（不使用 full_page 以避免超时）
            try:
                await page.screenshot(path="supabase_page.png", timeout=10000)
                print("✅ 已截图保存到 supabase_page.png")
            except:
                print("⚠️  截图失败，继续...")

            # 尝试点击 Connection pooling 标签
            print("\n🔍 查找 Connection Pooling 标签...")

            # 方法1: 尝试多种选择器
            selectors = [
                'button:has-text("Connection pooling")',
                'text="Connection pooling"',
                '[role="tab"]:has-text("Connection pooling")',
                'div:has-text("Connection pooling")',
            ]

            clicked = False
            for selector in selectors:
                try:
                    await page.click(selector, timeout=3000)
                    print(f"✅ 成功点击 Connection pooling 标签")
                    clicked = True
                    await asyncio.sleep(3)
                    break
                except:
                    continue

            if not clicked:
                print("⚠️  未能点击标签，尝试直接提取...")

            # 再次截图
            try:
                await page.screenshot(path="supabase_page_after_click.png", timeout=10000)
                print("✅ 已截图保存到 supabase_page_after_click.png")
            except:
                print("⚠️  截图失败，继续...")

            # 获取页面内容
            print("\n🔍 分析页面内容...")
            page_content = await page.content()

            # 保存 HTML 以便调试
            with open("supabase_page.html", "w", encoding="utf-8") as f:
                f.write(page_content)
            print("✅ 页面 HTML 已保存到 supabase_page.html")

            # 查找包含 6543 端口的连接字符串
            patterns = [
                r'postgresql://[^:]+:[^@]+@[^:]+:6543/[^\s<>"\']+',
                r'postgres://[^:]+:[^@]+@[^:]+:6543/[^\s<>"\']+',
            ]

            for pattern in patterns:
                matches = re.findall(pattern, page_content)
                if matches:
                    connection_string = matches[0]
                    # 清理 HTML 实体
                    connection_string = connection_string.replace('&quot;', '').replace('&#x27;', '').replace('&amp;', '&')
                    break

            if connection_string:
                print(f"\n✅ 找到 Connection Pooling 连接字符串!")
                print(f"   前50字符: {connection_string[:50]}...")
                print(f"   后20字符: ...{connection_string[-20:]}")

                # 编码密码中的特殊字符
                if '://' in connection_string:
                    parts = connection_string.split('://', 1)
                    if len(parts) == 2:
                        protocol = parts[0]
                        rest = parts[1]

                        # 分离认证信息和主机信息
                        if '@' in rest:
                            # 找到最后一个 @ (这是主机前的分隔符)
                            last_at = rest.rfind('@')
                            auth = rest[:last_at]
                            host = rest[last_at+1:]

                            # 编码认证信息中的特殊字符
                            if ':' in auth:
                                username, password = auth.split(':', 1)
                                # 编码密码中的 @
                                password = password.replace('@', '%40')
                                connection_string = f"{protocol}://{username}:{password}@{host}"
                                print(f"\n✅ 已编码密码中的特殊字符")

                print(f"\n最终连接字符串: {connection_string}")
            else:
                print("\n❌ 未找到 Connection Pooling 连接字符串")
                print("请查看截图和 HTML 文件，手动查找连接字符串")

        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()

        finally:
            await browser.close()
            print("\n✅ 浏览器已关闭")

    # 如果找到了连接字符串，更新 GitHub Secret
    if connection_string:
        print("\n🔐 更新 GitHub Secret...")
        try:
            # 使用 gh CLI 更新 secret
            result = subprocess.run(
                ['gh', 'secret', 'set', 'DATABASE_URL', '-b', connection_string],
                cwd='/Users/chenanfan/TrendRadar-Dashboard',
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("✅ DATABASE_URL Secret 已成功更新!")

                # 触发 workflow
                print("\n🚀 触发 GitHub Actions workflow...")
                subprocess.run(
                    ['gh', 'workflow', 'run', 'crawler.yml'],
                    cwd='/Users/chenanfan/TrendRadar-Dashboard'
                )
                print("✅ Workflow 已触发!")
            else:
                print(f"❌ 更新 Secret 失败: {result.stderr}")
                print(f"\n请手动运行以下命令:")
                print(f'gh secret set DATABASE_URL -b "{connection_string}"')
        except Exception as e:
            print(f"❌ 更新 Secret 时出错: {e}")
            print(f"\n请手动运行以下命令:")
            print(f'gh secret set DATABASE_URL -b "{connection_string}"')
    else:
        print("\n⚠️  未能自动获取连接字符串，请查看生成的文件手动处理")

if __name__ == "__main__":
    asyncio.run(main())
