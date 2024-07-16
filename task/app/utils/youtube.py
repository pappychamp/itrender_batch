import os

# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ApiKey
from logs.logs_setting import logger

API_KEY = os.environ.get("YOUTUBE_API_KEY")


class YoutubeAPI:

    def __init__(self):
        self.api_key = ApiKey(API_KEY)
        self.youtube_api_name = "youtube"
        self.youtube_api_version = "v3"

    async def fetch_video(self):
        async with Aiogoogle(api_key=self.api_key) as aiogoogle:
            try:
                youtube = await aiogoogle.discover(self.youtube_api_name, self.youtube_api_version)
                request = youtube.videos.list(
                    part="snippet,player,topicDetails,statistics",
                    chart="mostPopular",
                    regionCode="JP",
                    hl="ja",
                    maxResults=20,
                )
                response = await aiogoogle.as_api_key(request)
                return response
            except Exception as e:
                logger.error(e)
