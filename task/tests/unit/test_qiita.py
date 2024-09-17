import aiohttp
import feedparser
import pytest
from aioresponses import aioresponses
from app.utils.qiita import QiitaAPI


@pytest.fixture
def qiita_api():
    return QiitaAPI()


@pytest.mark.asyncio
async def test_qiita_fetch_rss_success(qiita_api):
    """
    fetch_rssメソッドの正常テスト
    """
    # RSS フィードのモック
    rss_feed = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
        <channel>
            <title>Qiita 人気記事</title>
            <link>https://qiita.com/popular-items</link>
            <description>Qiita 人気記事フィード</description>
            <item>
                <title>Example Article</title>
                <link>https://qiita.com/items/example_id</link>
                <pubDate>2024-07-04T07:27:46+09:00</pubDate>
            </item>
        </channel>
        </rss>"""
    with aioresponses() as m:
        m.get(qiita_api.rss_url, body=rss_feed)

        # テスト
        async with aiohttp.ClientSession() as session:
            data = await qiita_api.fetch_rss(session)

        assert data is not None
        assert "entries" in data


@pytest.mark.asyncio
async def test_fetch_rss_invalid_rss(mocker, qiita_api):
    """
    fetch_rssメソッドbozo=1の例外テスト
    """
    mock_response = {"bozo": 1}

    mocker.patch("feedparser.parse", return_value=mock_response)

    async with aiohttp.ClientSession() as session:
        with pytest.raises(ValueError) as exc_info:
            await qiita_api.fetch_rss(session)
        assert "RSSデータの中身が空です" in str(exc_info.value)


@pytest.mark.asyncio
async def test_qiita_fetch_article_tag_success(qiita_api):
    """
    fetch_article_tagメソッドの正常テスト
    """
    article_id = "example_id"
    url = f"{qiita_api.api_url}/items/{article_id}"
    mock_response = {"tags": [{"name": "Python", "versions": []}, {"name": "自動化", "versions": []}]}
    with aioresponses() as m:
        m.get(url, payload=mock_response, status=200)

        # テスト
        async with aiohttp.ClientSession() as session:
            data = await qiita_api.fetch_article_tag(session, article_id)
        assert data is not None
        assert "tags" in data


@pytest.mark.asyncio
async def test_fetch_article_tag_no_tags(qiita_api):
    """
    fetch_article_tagメソッドのデータの中身が空のテスト
    """
    article_id = "example_id"
    url = f"{qiita_api.api_url}/items/{article_id}"
    with aioresponses() as m:
        # タグがないデータのモック
        no_tag_data = {"id": article_id, "tags": []}
        m.get(url, payload=no_tag_data, status=200)

        async with aiohttp.ClientSession() as session:
            with pytest.raises(ValueError, match="データまたはtagデータの中身が空です"):
                await qiita_api.fetch_article_tag(session, article_id)


@pytest.mark.asyncio
async def test_fetch_article_tag_network_error(qiita_api):
    """
    fetch_article_tagメソッドの例外発生時のテスト
    """
    article_id = "example_id"
    url = f"{qiita_api.api_url}/items/{article_id}"
    with aioresponses() as m:
        # ネットワークエラーのモック
        m.get(url, exception=aiohttp.ClientError("ネットワークエラー"))

        async with aiohttp.ClientSession() as session:
            with pytest.raises(Exception, match="ネットワークエラー"):
                await qiita_api.fetch_article_tag(session, article_id)


@pytest.mark.asyncio
async def test_fetch_article_success(mocker, qiita_api):
    """
    fetch_articleメソッドの正常テスト
    """
    rss_url = qiita_api.rss_url
    with aioresponses() as m:
        # 有効なRSSフィードのモック
        valid_rss_feed = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
        <channel>
            <title>Qiita 人気記事</title>
            <link>https://qiita.com/popular-items</link>
            <description>Qiita 人気記事フィード</description>
            <item>
                <title>Example Article</title>
                <link>https://qiita.com/items/example_id</link>
                <pubDate>2024-07-04T07:27:46+09:00</pubDate>
            </item>
        </channel>
        </rss>"""
        m.get(rss_url, body=valid_rss_feed, status=200)

        # 各記事のタグデータのモック
        article_id = "example_id"
        tags_url = f"{qiita_api.api_url}/items/{article_id}"
        valid_tag_data = {"tags": [{"name": "Python"}, {"name": "Django"}]}
        m.get(tags_url, payload=valid_tag_data, status=200)

        async with aiohttp.ClientSession():
            # fetch_rssとfetch_article_tagメソッドをモックする
            mocker.patch.object(QiitaAPI, "fetch_rss", return_value=feedparser.parse(valid_rss_feed))
            mocker.patch.object(QiitaAPI, "fetch_article_tag", return_value=valid_tag_data)
            data = await qiita_api.fetch_article()

        # 結果の検証
        assert data is not None
        assert "articles" in data
        assert len(data["articles"]) > 0
        article = data["articles"][0]
        assert "title" in article
        assert "link" in article
        assert "updated" in article
        assert "tags" in article


@pytest.mark.asyncio
async def test_fetch_article_invalid_link_format(mocker, qiita_api):
    """
    fetch_articleメソッドのmatchのエラー
    """
    rss_url = qiita_api.rss_url
    with aioresponses() as m:
        # 無効なリンク形式のRSSフィードのモック
        invalid_link_rss_feed = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
        <channel>
            <title>Qiita 人気記事</title>
            <link>https://qiita.com/popular-items</link>
            <description>Qiita 人気記事フィード</description>
            <item>
                <title>Example Article</title>
                <link>https://qiita.com/invalid-link-format</link>
                <pubDate>Wed, 01 Jan 2024 00:00:00 +0000</pubDate>
            </item>
        </channel>
        </rss>"""
        m.get(rss_url, body=invalid_link_rss_feed, status=200)

        async with aiohttp.ClientSession():
            mocker.patch.object(QiitaAPI, "fetch_rss", return_value=feedparser.parse(invalid_link_rss_feed))
            with pytest.raises(ValueError, match="無効なリンク形式です"):
                await qiita_api.fetch_article()


@pytest.mark.asyncio
async def test_fetch_article_invalid_rss(mocker, qiita_api):
    """
    fetch_articleメソッドのentriesデータが空の場合のテスト
    """
    rss_url = qiita_api.rss_url
    with aioresponses() as m:
        # 無効なRSSフィードのモック
        invalid_rss_feed = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
        <channel>
            <title>Qiita 人気記事</title>
            <link>https://qiita.com/popular-items</link>
            <description>Qiita 人気記事フィード</description>
        </channel>
        </rss>"""
        m.get(rss_url, body=invalid_rss_feed, status=200)

        async with aiohttp.ClientSession():
            mocker.patch.object(QiitaAPI, "fetch_rss", return_value=feedparser.parse(invalid_rss_feed))
            with pytest.raises(ValueError, match="データまたはentriesデータの中身が空です"):
                await qiita_api.fetch_article()


@pytest.mark.asyncio
async def test_fetch_article_network_error(mocker, qiita_api):
    """
    fetch_articleメソッドの例外発生時のテスト
    """
    rss_url = qiita_api.rss_url
    with aioresponses() as m:
        # ネットワークエラーのモック
        m.get(rss_url, exception=aiohttp.ClientError("ネットワークエラー"))

        async with aiohttp.ClientSession():
            mocker.patch.object(QiitaAPI, "fetch_rss", side_effect=ValueError("RSSフィードの取得に失敗しました"))
            with pytest.raises(ValueError, match="RSSフィードの取得に失敗しました"):
                await qiita_api.fetch_article()


@pytest.mark.asyncio
async def test_fetch_article_image_success(qiita_api):
    """
    fetch_article_imageメソッドの正常テスト
    """
    # サンプルURLを用意
    sample_url = "https://qiita.com/test/items/test"
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <head>
                <meta property="og:image" content="test_content">
            </head>
        </html>
        """

    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get(sample_url, body=sample_html)
        # テスト
        response = await qiita_api.fetch_article_image(sample_url)
    assert response == "test_content"


@pytest.mark.asyncio
async def test_fetch_article_image_no_a_tag(qiita_api):
    """
    fetch_article_imageメソッドのmetaタグがない場合の正常テスト
    """
    # サンプルURLを用意
    sample_url = "https://qiita.com/test/items/test"
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <head>
                <metas property="og:image" content="test_content">
            </head>
        </html>
        """

    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get(sample_url, body=sample_html)
        # テスト
        response = await qiita_api.fetch_article_image(sample_url)
    assert response is None


@pytest.mark.asyncio
async def test_fetch_article_image_exception(qiita_api):
    """
    fetch_article_imageメソッドの例外発生時のテスト
    """
    sample_url = "https://qiita.com/test/items/test"

    with aioresponses() as m:
        m.get(sample_url, exception=aiohttp.ClientError())
        # テスト
        with pytest.raises(aiohttp.ClientError):
            await qiita_api.fetch_article_image(sample_url)
