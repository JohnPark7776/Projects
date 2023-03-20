import asyncio
from playwright.async_api import async_playwright, TimeoutError as TE
from bs4 import BeautifulSoup as bs
import requests


results = {}

def parse_item(html_page):
    """Parses through a string to grab Img Src or Video Src

    Args:
        html_page (str): html str
    """
    soup = bs(html_page, 'html.parser')
    data = soup.find_all('img')
    for item in data:
        if str(item['class']).replace(' ', "") != "['xh8yej3','xl1xv1r','x5yr21d']":
            image = requests.get(item['src'])
            results[image.content] = 'img'
    data = soup.find_all('video')
    for item in data:
        video = requests.get(item['src'])
        results[video.content] = 'vid'

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
                main = page.locator('div._aao_')
                for i in range(10):
                    try:
                        next_page = main.get_by_role('button',name='Next')
                        page.set_default_timeout(500)
                        for li in await main.locator('ul._acay').all():
                            parse_item(await li.inner_html())
                        await next_page.click()
                    except TE:
                        break
            await browser.close()
            return results
        except TE:
            await page.reload(wait_until='networkidle')
            try:
                if await page.is_enabled('div._aagv',timeout=1000):
                    content = await page.locator('div._aagv').inner_html()
            except TE:
                content = await page.locator(".x1lliihq > div > div > div").inner_html()
            parse_item(content)
            await browser.close()
            return results
