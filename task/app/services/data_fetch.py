from db.setting import Session
from logs.logs_setting import logger
from services.data_mapping import (
    data_mapping,
    qiita_data_mapping,
    techplus_data_mapping,
    thinkit_data_mapping,
    yahoo_data_mapping,
    youtube_data_mapping,
    zenn_data_mapping,
)
from services.data_validate import TrendDataModel
from services.db_service import create_trend_data, get_site_id
from utils.qiita import QiitaAPI
from utils.techplus import TechplusAPI
from utils.thinkit import ThinkitAPI
from utils.yahoo import YahooAPI
from utils.youtube import YoutubeAPI
from utils.zenn import ZennAPI

youtube_api = YoutubeAPI()
zenn_api = ZennAPI()
qiita_api = QiitaAPI()
yahoo_api = YahooAPI()
thinkit_api = ThinkitAPI()
techplus_api = TechplusAPI()


async def fetch_data(api_fetch_func, site_name, data_mapping_func):
    try:
        async with Session() as session:
            # データ取得
            data = await api_fetch_func()
            site_id = await get_site_id(session, site_name=site_name)
            # データ処理
            mapped_data = await data_mapping(site_id, data.get("items") or data.get("articles"), data_mapping_func)
            # バリデーション
            validated_data = [TrendDataModel(**data).model_dump() for data in mapped_data]
            # 保存
            response = await create_trend_data(session, validated_data)
            return {site_name: response}
    except Exception as e:
        logger.error(e, exc_info=True)


async def fetch_youtube_data():
    return await fetch_data(youtube_api.fetch_video, site_name="youtube", data_mapping_func=youtube_data_mapping)


async def fetch_zenn_data():
    return await fetch_data(zenn_api.fetch_article, site_name="zenn", data_mapping_func=zenn_data_mapping)


async def fetch_qiita_data():
    return await fetch_data(qiita_api.fetch_article, site_name="qiita", data_mapping_func=qiita_data_mapping)


async def fetch_yahoo_data():
    return await fetch_data(yahoo_api.fetch_article, site_name="yahoo", data_mapping_func=yahoo_data_mapping)


async def fetch_thinkit_data():
    return await fetch_data(thinkit_api.fetch_article, site_name="thinkit", data_mapping_func=thinkit_data_mapping)


async def fetch_techplus_data():
    return await fetch_data(techplus_api.fetch_article, site_name="techplus", data_mapping_func=techplus_data_mapping)
