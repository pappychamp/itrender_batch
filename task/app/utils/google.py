import asyncio

from pytrends.request import TrendReq


class GoogleAPI:

    async def fetch_trending_searches(self):
        pytrends = TrendReq(hl="ja-JP", tz=540)
        a = pytrends.trending_searches(pn="japan")
        return a.values.tolist()

    async def fetch_related_queries(self, keyword):
        pytrends = TrendReq(hl="ja-JP", tz=540)
        pytrends.build_payload([keyword], cat=0, timeframe="now 1-d", geo="JP")
        b = pytrends.related_queries()
        return b.get(keyword).get("top").values.tolist()

    async def fetch_trend(self):
        try:
            # response_data = {"search_trends": []}
            response_data = []
            trend_list = await self.fetch_trending_searches()
            print(trend_list)
            for trend in trend_list:
                for keyword in trend:
                    search_trend_related = await self.fetch_related_queries(keyword)
                    search_trend = {"title": keyword, "tag": [item[0] for item in search_trend_related]}
                    response_data.append(search_trend)
            return {"search_trends": response_data}
        except Exception as e:
            print(f"error={e}")


async def main():
    instance = GoogleAPI()
    data = await instance.fetch_trend()
    print(data)


if __name__ == "__main__":
    asyncio.run(main())
