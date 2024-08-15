import asyncio

import aiohttp
from bs4 import BeautifulSoup


class YahooAPI:

    def __init__(self) -> None:
        self.url = "https://news.yahoo.co.jp/ranking/access/news"

    async def fetch_article(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                ranking = soup.find_all(class_="newsFeed_item_title")
                for item in ranking:
                    print(item.get_text())


async def main():
    instance = YahooAPI()
    await instance.fetch_article()


if __name__ == "__main__":
    asyncio.run(main())
