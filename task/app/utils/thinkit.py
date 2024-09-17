import asyncio

import aiohttp
from bs4 import BeautifulSoup


class ThinkitAPI:

    def __init__(self) -> None:
        self.url = "https://thinkit.co.jp/ranking/daily"

    async def fetch_article(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:

                    response.raise_for_status()
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    articles = soup.find_all("div", class_="views-field views-field-title")
                    if articles:
                        pass
                    else:
                        raise ValueError(f"データまたはarticlesデータの中身が空です:{articles}")

                    data = []
                    for article in articles[:20]:
                        a_tag_element = article.find("a")
                        if a_tag_element:
                            url = a_tag_element["href"]
                            # stripで空白文字（半角スペース、タブ、改行など）を削除。replaceで全角(\u3000)を半角スペースに置き換える
                            title = a_tag_element.get_text(strip=True).replace("\u3000", " ")
                        else:
                            continue

                        data.append({"title": title, "url": url})
                    return {"articles": data}
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
    instance = ThinkitAPI()
    a = await instance.fetch_article_image("https://thinkit.co.jp/article/32300")
    print(a)


if __name__ == "__main__":
    asyncio.run(main())
