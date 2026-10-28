import sys, time, asyncio
from playwright.async_api import async_playwright

URLS = {
    "RtKM45drVxU": "https://youtube.com/shorts/RtKM45drVxU",
    "4LlXT5FO6Ik": "https://youtube.com/shorts/4LlXT5FO6Ik",
    "PtwMATZq98U": "https://youtube.com/shorts/PtwMATZq98U",
}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = await browser.new_context(viewport={"width": 720, "height": 1280},
                                        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")
        for key, url in URLS.items():
            page = await ctx.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(6000)
                await page.screenshot(path=f"{key}.png")
                # try to grab video frame too
                title = await page.title()
                print(f"{key}: {title}")
            except Exception as e:
                print(f"{key}: ERROR {e}")
            finally:
                await page.close()
        await browser.close()

asyncio.run(main())
