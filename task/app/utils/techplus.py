import asyncio

import aiohttp
from bs4 import BeautifulSoup


class TechplusAPI:

    def __init__(self) -> None:
        self.url = "https://news.mynavi.jp/techplus/ranking/"

    async def fetch_article(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:

                    response.raise_for_status()
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    articles = soup.find_all("a", class_="rankingtList_listNode_link")
                    if articles:
                        pass
                    else:
                        raise ValueError(f"データまたはarticlesデータの中身が空です:{articles}")

                    data = []
                    for article in articles[:20]:
                        url = article["href"]
                        title_element = article.find("h3", class_="rankingtList_listNode_catch")
                        if title_element:
                            # stripで空白文字（半角スペース、タブ、改行など）を削除。replaceで全角(\u3000)を半角スペースに置き換える
                            title = title_element.get_text(strip=True).replace("\u3000", " ")
                        else:
                            continue

                        data.append({"title": title, "url": url})
                    return {"articles": data}
            except Exception:
                raise


async def main():
    instance = TechplusAPI()
    await instance.fetch_article()


if __name__ == "__main__":
    asyncio.run(main())
