import asyncio

from logs.logs_setting import logger
from logs.sentry_setting import init_sentry
from services.data_fetch import fetch_qiita_data, fetch_youtube_data, fetch_zenn_data


async def main():
    try:
        response_list = await asyncio.gather(
            fetch_youtube_data(),
            fetch_qiita_data(),
            fetch_zenn_data(),
            # 上記処理のどれかで例外が起きても他の処理を続行する。(デフォルトのfalseの場合他の処理も途中で止まる。)
            return_exceptions=True,
        )
        logger.info(response_list)
    except Exception as e:
        logger.error(e, exc_info=True)


if __name__ == "__main__":
    init_sentry()
    asyncio.run(main())
