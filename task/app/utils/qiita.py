import asyncio
import os
import re

import aiohttp
import feedparser
from bs4 import BeautifulSoup

ACCESS_TOKEN = os.environ.get("QIITA_ACCESS_TOKEN")


class QiitaAPI:

    def __init__(self) -> None:
        self.rss_url = "https://qiita.com/popular-items/feed"
        self.api_url = "https://qiita.com/api/v2"
        self.headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    async def fetch_article(self):
        """
        rssによる人気記事の取得,apiによる各記事のtag取得
        """
        # rss処理
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                rss_response = await self.fetch_rss(session)
                # bozoはパースエラーがあったかどうかを示すフラグ
                if rss_response and rss_response.get("entries"):
                    response = []
                    articles = rss_response.get("entries")[:20]
                    tasks = []
                    for article in articles:
                        link = article.get("link", "")
                        match = re.search(r"/items/([a-zA-Z0-9]+)", link)
                        if match:
                            article_id = match.group(1)
                            # api処理
                            task = self.fetch_article_tag(session, article_id=article_id)
                            tasks.append(task)
                        else:
                            raise ValueError(f"無効なリンク形式です:{link}")
                    tags_data_list = await asyncio.gather(*tasks)
                    for article, tags_data in zip(articles, tags_data_list):
                        article.update(tags_data)
                        keys_to_extract = ["title", "link", "updated", "tags"]
                        extracted_dict = {key: article.get(key) for key in keys_to_extract}
                        response.append(extracted_dict)
                    return {"articles": response}
                else:
                    raise ValueError(f"データまたはentriesデータの中身が空です:{rss_response}")
        except Exception:
            raise

    async def fetch_rss(self, session):
        try:
            async with session.get(self.rss_url) as response:
                response.raise_for_status()
                data = feedparser.parse(await response.text())
                if data.get("bozo"):
                    raise ValueError(f"RSSデータの中身が空です:{data}")
                return data
        except Exception:
            raise

    async def fetch_article_tag(self, session, article_id):
        url = f"{self.api_url}/items/{article_id}"
        try:
            async with session.get(url, headers=self.headers) as response:
                response.raise_for_status()
                data = await response.json()
                if not data or not data.get("tags"):
                    raise ValueError(f"データまたはtagデータの中身が空です:{data}")
                return data
        except Exception:
            raise

    async def fetch_article_image(self, url) -> str | None:
        """
        スクレイピングによるimageの取得
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:

                    response.raise_for_status()
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    ogp_image = soup.find("meta", attrs={"property": "og:image"})
                    if ogp_image:
                        return ogp_image.get("content")
                    else:
                        return
            except Exception:
                raise


async def main():
    instance = QiitaAPI()
    a = await instance.fetch_article_image("")
    print(a)


if __name__ == "__main__":
    asyncio.run(main())
