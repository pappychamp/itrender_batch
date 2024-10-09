import asyncio

import matplotlib.pyplot as plt
import pandas as pd
from pytrends.request import TrendReq


class GoogleAPI:

    async def fetch_interest_over_time(self, kw_list):
        pytrends = TrendReq(hl="ja-JP", tz=540)
        pytrends.build_payload(kw_list, timeframe="2024-08-20 2024-09-20", geo="JP")
        df1 = pytrends.interest_over_time()
        return df1

    async def fetch_interest_over_times(self, kw_list):
        all_data = pd.DataFrame()
        pytrends = TrendReq(hl="ja-JP", tz=540)
        # 5つずつのグループに分けてリクエストを送る
        for i in range(0, len(kw_list), 5):
            group = kw_list[i : i + 5]
            pytrends.build_payload(group, timeframe="2024-08-20 2024-09-20", geo="JP")
            df = pytrends.interest_over_time()
            all_data = pd.concat([all_data, df], axis=1)  # 結果を結合

        # 重複した "isPartial" 列を削除
        if "isPartial" in all_data.columns:
            all_data = all_data.drop(columns=["isPartial"])

        return all_data

    # async def fetch_google_suggestions(self, query):
    #     url = f"https://suggestqueries.google.com/complete/search?output=firefox&q={query}&hl=ja"
    #     async with aiohttp.ClientSession() as session:
    #         try:
    #             print(self.cache)
    #             async with session.get(url) as response:
    #                 response.raise_for_status()
    #                 data = await response.json(content_type="text/javascript")
    #                 # if not data or not data.get("articles"):
    #                 #     raise ValueError(f"データまたはarticlesデータの中身が空です:{data}")
    #                 self.cache[query] = data
    #             return data
    #         except Exception as e:
    #             print(e)

    # async def fetch_related_queries(self, keyword):
    #     pytrends = TrendReq(hl="ja-JP", tz=540)
    #     pytrends.build_payload([keyword], cat=0, timeframe="now 1-d", geo="JP")
    #     b = pytrends.related_queries()
    #     return b.get(keyword).get("top").values.tolist()

    # async def fetch_trend(self):
    #     try:
    #         kw_list = ["Python", "Java", "Ruby", "Javascript", "PHP"]
    #         response_data = []
    #         trend_list = await self.fetch_interest_over_time(kw_list)
    #         print(trend_list)
    #         for keyword in kw_list:
    #             search_trend_related = await self.fetch_related_queries(keyword)
    #             search_trend = {"title": keyword, "tag": [item[0] for item in search_trend_related]}
    #             response_data.append(search_trend)
    #         return {"search_trends": response_data}
    #     except Exception as e:
    #         print(f"error={e}")

    def plot_interest_over_time(self, df, kw_list):
        # カラーマップを使って色を自動設定
        plt.figure(figsize=(12, 8))
        cmap = plt.get_cmap("tab10")
        num_colors = min(len(kw_list), cmap.N)
        colors = [cmap(i) for i in range(num_colors)]

        for i, kw in enumerate(kw_list):
            if kw in df.columns:
                plt.plot(df.index, df[kw], label=kw, color=colors[i % num_colors])

        plt.title(f"Interest Over Time for {', '.join(kw_list)}", fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Interest", fontsize=12)
        plt.legend(title="Keywords", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


async def main():
    instance = GoogleAPI()
    kw_list = ["Python", "Java", "Ruby", "Javascript", "PHP", "Visual Basic .NET", "Go", "Swift", "C#", "Kotlin"]
    data1 = await instance.fetch_interest_over_times(kw_list)
    # data2 = await instance.fetch_interest_over_time(["Visual Basic .NET", "Go", "Swift", "C#", "Kotlin"])
    instance.plot_interest_over_time(data1, kw_list)
    # data1.plot(figsize=(15, 3), lw=0.7)
    # suggestions = await instance.fetch_google_suggestions("Python")
    # print(suggestions)


if __name__ == "__main__":
    asyncio.run(main())
