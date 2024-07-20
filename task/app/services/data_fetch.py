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

youtube_api = YoutubeAPI()
zenn_api = ZennAPI()
qiita_api = QiitaAPI()


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
            return response
    except Exception as e:
        logger.error(e, exc_info=True)


async def fetch_youtube_data():
    return await fetch_data(youtube_api.fetch_video, site_name="youtube", data_mapping_func=youtube_data_mapping)


async def fetch_zenn_data():
    return await fetch_data(zenn_api.fetch_article, site_name="zenn", data_mapping_func=zenn_data_mapping)


async def fetch_qiita_data():
    return await fetch_data(qiita_api.fetch_article, site_name="qiita", data_mapping_func=qiita_data_mapping)
