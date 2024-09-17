import asyncio
import re
from datetime import datetime, timedelta, timezone

import aiohttp
from bs4 import BeautifulSoup


class YahooAPI:

    def __init__(self) -> None:
        self.url = "https://news.yahoo.co.jp/ranking/access/news/it-science"
        self.current_year = datetime.now().year

    async def format_time(self, time):
        # 曜日の部分を削除
        published_at = re.sub(r"\(.*?\)", "", time)
        dt = datetime.strptime(published_at, "%m/%d %H:%M")
        # 年を補完
        dt = dt.replace(year=self.current_year)
        # タイムゾーン(+09:00)を追加
        dt_with_tz = dt.replace(tzinfo=timezone(timedelta(hours=9)))
        # フォーマットされた文字列を出力
        formatted_time = dt_with_tz.strftime("%Y-%m-%d %H:%M:%S.%f %z")
        return formatted_time

    async def fetch_article(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:

                    response.raise_for_status()
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    articles = soup.find_all("a", class_="newsFeed_item_link")
                    if articles:
                        pass
                    else:
                        raise ValueError(f"データまたはarticlesデータの中身が空です:{articles}")

                    data = []
                    for article in articles:
                        url = article["href"]
                        time_element = article.find("time")
                        if time_element:
                            time = time_element.get_text()
                            published_at = await self.format_time(time)
                        else:
                            continue

                        title_element = article.find(class_="newsFeed_item_title")
                        if title_element:
                            # stripで空白文字（半角スペース、タブ、改行など）を削除。replaceで全角(\u3000)を半角スペースに置き換える
                            title = title_element.get_text(strip=True).replace("\u3000", " ")
                        else:
                            continue

                        data.append({"title": title, "url": url, "published_at": published_at})
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
    instance = YahooAPI()
    a = await instance.fetch_article_image("https://news.yahoo.co.jp/articles/efeb7c713a6f026f6a275966f5b7e41de5392b1b")
    print(a)


if __name__ == "__main__":
    asyncio.run(main())
