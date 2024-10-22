from dateutil import parser
from utils.qiita import QiitaAPI
from utils.techplus import TechplusAPI
from utils.thinkit import ThinkitAPI
from utils.yahoo import YahooAPI
from utils.zenn import ZennAPI

zenn_api = ZennAPI()
qiita_api = QiitaAPI()
yahoo_api = YahooAPI()
thinkit_api = ThinkitAPI()
techplus_api = TechplusAPI()


async def data_mapping(site_id, data_list, data_mapping_func):
    """
    指定されたサイトのデータを処理。

    Args:
        site_id (uuidオブジェクト): サイトのid
        data_list (list): 処理および保存するデータアイテムのリスト。
        data_mapping_func (function): 生データを保存に必要な形式にマッピングする関数。

    Returns:
        mapped_data: データ処理後のデータ
    """
    try:
        mapped_data = [await data_mapping_func(site_id, data, index) for index, data in enumerate(data_list[:20], start=1)]
        return mapped_data
    except Exception:
        raise


async def zenn_data_mapping(site_id, article_data, ranking):
    title = article_data.get("title")
    path = article_data.get("path", "")
    url = f"https://zenn.dev{path}"
    published_at = article_data.get("published_at")

    # 共通のデータ部分
    article_data_dict = {
        "site_id": site_id,
        "title": title,
        "ranking": ranking,
        "url": url,
        "published_at": parser.parse(published_at),
    }

    # 追加データ取得
    if path:
        image_and_tag_dict = await zenn_api.fetch_article_image_and_tag(url)
        tags = image_and_tag_dict.get("tags", [])
        unique_tags = list(set(tags))
        article_data_dict.update(
            {
                "tags": [{"name": tag} for tag in unique_tags],
                "image_url": image_and_tag_dict.get("image_url"),
            }
        )

    return article_data_dict


async def youtube_data_mapping(site_id, video_data, ranking):
    snippet = video_data.get("snippet", {})
    category_id = snippet.get("categoryId")
    title = snippet.get("title")
    tags = snippet.get("tags", [])
    published_at = snippet.get("publishedAt")
    url = f'https://www.youtube.com/watch?v={video_data.get("id","")}'
    embed_html = video_data.get("player").get("embedHtml")
    image_url = snippet.get("thumbnails", {}).get("standard", {}).get("url")
    unique_tags = list(set(tags))

    video_data_dict = {
        "site_id": site_id,
        "title": title,
        "ranking": ranking,
        "tags": [{"name": tag} for tag in unique_tags],
        "url": url,
        "published_at": parser.parse(published_at),
        "embed_html": embed_html,
        "image_url": image_url,
        "category": category_id,
    }
    return video_data_dict


async def qiita_data_mapping(site_id, article_data, ranking):
    title = article_data.get("title")
    tags = article_data.get("tags", [])
    url = article_data.get("link", "")
    published_at = article_data.get("updated")
    unique_tags = list({tag["name"]: tag for tag in tags}.values())

    article_data_dict = {
        "site_id": site_id,
        "title": title,
        "ranking": ranking,
        "tags": unique_tags,
        "url": url,
        "published_at": parser.parse(published_at),
    }

    # 追加データ取得
    if url:
        image_url = await qiita_api.fetch_article_image(url)
        article_data_dict.update({"image_url": image_url})
    return article_data_dict


async def yahoo_data_mapping(site_id, article_data, ranking):
    url = article_data.get("url", "")
    published_at = article_data.get("published_at")

    article_data_dict = {
        "site_id": site_id,
        "ranking": ranking,
        "url": url,
        "published_at": parser.parse(published_at),
    }
    # 追加データ取得
    if url:
        title_image_url_data = await yahoo_api.fetch_article_title_and_image(url)
        article_data_dict.update(
            {
                "title": title_image_url_data.get("title"),
                "image_url": title_image_url_data.get("image_url"),
            }
        )
    return article_data_dict


async def thinkit_data_mapping(site_id, article_data, ranking):
    title = article_data.get("title")
    path = article_data.get("url", "")
    url = f"https://thinkit.co.jp{path}"

    article_data_dict = {
        "site_id": site_id,
        "title": title,
        "ranking": ranking,
        "url": url,
    }
    # 追加データ取得
    if path:
        image_url = await thinkit_api.fetch_article_image(url)
        article_data_dict.update({"image_url": image_url})
    return article_data_dict


async def techplus_data_mapping(site_id, article_data, ranking):
    title = article_data.get("title")
    path = article_data.get("url", "")
    url = f"https://news.mynavi.jp{path}"

    article_data_dict = {
        "site_id": site_id,
        "title": title,
        "ranking": ranking,
        "url": url,
    }
    # 追加データ取得
    if path:
        image_url = await techplus_api.fetch_article_image(url)
        article_data_dict.update({"image_url": image_url})
    return article_data_dict
