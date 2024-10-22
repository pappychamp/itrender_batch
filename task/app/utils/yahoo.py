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
                    articles = soup.find_all("li", class_=re.compile(r"newsFeed_item"))
                    if articles:
                        pass
                    else:
                        raise ValueError(f"データまたはarticlesデータの中身が空です:{articles}")

                    data = []
                    for article in articles:
                        a_tag = article.find("a")
                        if a_tag:
                            url = a_tag["href"]
                        else:
                            raise ValueError("a_tagがありません")
                        time_element = article.find("time")
                        if time_element:
                            time = time_element.get_text()
                            published_at = await self.format_time(time)
                        else:
                            continue

                        data.append({"url": url, "published_at": published_at})
                    return {"articles": data}
            except Exception:
                raise

    async def fetch_article_title_and_image(self, url) -> str | None:
        """
        スクレイピングによるimageの取得
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:

                    response.raise_for_status()
                    html = await response.text()

                    soup = BeautifulSoup(html, "html.parser")
                    title_element = soup.find("article") and soup.find("article").find("header") and soup.find("article").find("header").find("h1")
                    if title_element:
                        # stripで空白文字（半角スペース、タブ、改行など）を削除。replaceで全角(\u3000)を半角スペースに置き換える
                        title = title_element.get_text(strip=True).replace("\u3000", " ")
                    else:
                        raise ValueError("title_elementデータの中身が空です")

                    ogp_image = soup.find("meta", attrs={"property": "og:image"})
                    if ogp_image:
                        image_url = ogp_image.get("content")
                    else:
                        image_url = None
                    article_data = {"title": title, "image_url": image_url}
                    return article_data
            except Exception:
                raise


async def main():
    instance = YahooAPI()
    # a = await instance.fetch_article_title_and_image("https://news.yahoo.co.jp/articles/ad334290b20b944a967d19af396855201329c9c2")
    a = await instance.fetch_article()
    print(a)


if __name__ == "__main__":
    asyncio.run(main())
