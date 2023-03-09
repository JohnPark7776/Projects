import asyncio
from playwright.async_api import async_playwright, TimeoutError as TE
from bs4 import BeautifulSoup as bs
import time

results = set()
def parse_item(html_page):
    """Parses through a string to grab Img Src

    Args:
        html_page (str): html str
    """
    soup = bs(html_page, 'html.parser')
    data = soup.find_all('img')
    for photo in data:
        results.add(photo['src'])

async def start_this(link):
    """Opens a browser to selected Instagram Post
    First try is to check if there's a 'Next' Button
    Second try is to check if reached the end of the Post

    Args:
        link (str): IG URL

    Returns:
        Set: Returns the Img Src
    """
    results.clear()
    url = link
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        try:
            if await page.is_enabled('div._aao_',timeout=5000):
                for i in range(10):
                    try:
                        next_page = page.locator('div._aao_').get_by_role('button',name='Next')
                        page.set_default_timeout(2000)
                        for li in await page.locator('div._aao_').filter(has=page.get_by_role('listitem')).all():
                            parse_item(await li.inner_html())
                        await next_page.click()
                        time.sleep(.55)
                    except TE:
                        break
            await browser.close()
        except TE:
            try:
                content = await page.locator('article').locator('div._aagv').inner_html()
            except:
                content = await page.locator('div._aagv').inner_html()
            parse_item(content)
            await browser.close()
    return results
