import asyncio

import aiohttp


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


async def main():
    instance = ZennAPI()
    data = await instance.fetch_article()
    print(type(data))


if __name__ == "__main__":
    asyncio.run(main())
