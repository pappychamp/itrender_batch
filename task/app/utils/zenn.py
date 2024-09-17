import re

import aiohttp
from bs4 import BeautifulSoup


class ZennAPI:

    async def fetch_article(self):
        """
        apiによる人気記事の取得
        """
        url = "https://zenn.dev/api/articles"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                if not data or not data.get("articles"):
                    raise ValueError(f"データまたはarticlesデータの中身が空です:{data}")
                return data
            except Exception:
                raise

    async def fetch_article_image_and_tag(self, url):
        """
        fetch_article_image,fetch_article_tagの実行
        """

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:

                    response.raise_for_status()
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    image_url = await self.fetch_article_image(soup)
                    tags = await self.fetch_article_tag(soup)
                    return {"image_url": image_url, "tags": tags}
            except Exception:
                raise

    async def fetch_article_image(self, soup) -> str | None:
        """
        スクレイピングによるimageの取得
        """
        try:
            ogp_image = soup.find("meta", attrs={"property": "og:image"})
            if ogp_image:
                return ogp_image.get("content")
            else:
                return
        except Exception:
            raise

    async def fetch_article_tag(self, soup) -> list[str]:
        """
        スクレイピングによるtagの取得
        """
        try:
            tag_elements = soup.find_all("div", class_=re.compile(r"^View_topicName"))
            if tag_elements:
                return [tag_element.get_text(strip=True) for tag_element in tag_elements]
            return tag_elements

        except Exception:
            raise
