import asyncio
import json
import time

from db.setting import Session
from logs.logs_setting import logger
from services.data_mapping import (
    data_mapping,
    qiita_data_mapping,
    youtube_data_mapping,
    zenn_data_mapping,
)
from services.data_validate import TrendDataModel
from services.db_service import create_trend_data, get_site_id
from utils.qiita import QiitaAPI
from utils.youtube import YoutubeAPI
from utils.zenn import ZennAPI
from pydantic import ValidationError


async def main():
    try:
        youtube_api = YoutubeAPI()
        zenn_api = ZennAPI()
        qiita_api = QiitaAPI()

        async def fetch_youtube_data():
            async with Session() as session:
                print(f"Session in task {asyncio.current_task()}: {session}")
                videos_data = await youtube_api.fetch_video()
                site_id = await get_site_id(session, site_name="youtube")
                # データ処理
                mapped_data = await data_mapping(site_id, videos_data.get("items"), youtube_data_mapping)
                # validation処理
                validated_data = [TrendDataModel(**data).model_dump() for data in mapped_data]
                # 保存処理
                response = await create_trend_data(session, validated_data)
                return response

        async def fetch_zenn_data():
            async with Session() as session:
                print(f"Session in task {asyncio.current_task()}: {session}")
                articles_data = await zenn_api.fetch_article()
                site_id = await get_site_id(session, site_name="zenn")
                # データ処理
                mapped_data = await data_mapping(site_id, articles_data.get("articles"), zenn_data_mapping)
                # validation処理
                validated_data = [TrendDataModel(**data).model_dump() for data in mapped_data]
                # 保存処理
                response = await create_trend_data(session, validated_data)
                return response

        async def fetch_qiita_data():
            async with Session() as session:
                print(f"Session in task {asyncio.current_task()}: {session}")
                articles_data = await qiita_api.fetch_article()
                site_id = await get_site_id(session, site_name="qiita")
                # データ処理
                mapped_data = await data_mapping(site_id, articles_data.get("articles"), qiita_data_mapping)
                # validation処理
                validated_data = [TrendDataModel(**data).model_dump() for data in mapped_data]
                # 保存処理
                response = await create_trend_data(session, validated_data)
                return response

        start = time.perf_counter()
        response = await asyncio.gather(
            fetch_youtube_data(),
            fetch_zenn_data(),
            fetch_qiita_data(),
        )
        end1 = time.perf_counter()
        print(end1 - start)

        print(response)
    except ValidationError as e:
        logger.error(f"validation error発生:{e}")
    except Exception as e:
        logger.error(f"error発生:{e}")


async def handler():
    try:
        await main()
        print("$$$$$")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "hello world",
                }
            ),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": e}),
        }


if __name__ == "__main__":
    asyncio.run(handler())
