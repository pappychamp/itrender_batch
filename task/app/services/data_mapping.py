from dateutil import parser
from logs.logs_setting import logger


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
        mapped_data = [data_mapping_func(site_id, data) for data in data_list[:20]]
        return mapped_data
    except Exception:
        logger.error("データ処理に失敗")
        raise


def zenn_data_mapping(site_id, article_data):
    title = article_data.get("title")
    url = f"https://zenn.dev{article_data.get('path')}"
    published_at = article_data.get("published_at")

    article_data_dict = {
        "site_id": site_id,
        "title": title,
        "url": url,
        "published_at": parser.parse(published_at),
    }
    return article_data_dict


def youtube_data_mapping(site_id, video_data):
    snippet = video_data.get("snippet", {})
    category_id = snippet.get("categoryId")
    title = snippet.get("title")
    tags = snippet.get("tags", {})
    published_at = snippet.get("publishedAt")
    embed_html = video_data.get("player").get("embedHtml")

    video_data_dict = {
        "site_id": site_id,
        "title": title,
        "tags": [{"name": tag} for tag in tags],
        "published_at": parser.parse(published_at),
        "embed_html": embed_html,
        "category": category_id,
    }
    return video_data_dict


def qiita_data_mapping(site_id, article_data):
    title = article_data.get("title")
    tags = article_data.get("tags", [])
    url = article_data.get("link", "")
    published_at = article_data.get("updated")

    article_data_dict = {
        "site_id": site_id,
        "title": title,
        "tags": tags,
        "url": url,
        "published_at": parser.parse(published_at),
    }
    return article_data_dict
