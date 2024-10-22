import aiohttp
import pytest
from aioresponses import aioresponses
from app.utils.yahoo import YahooAPI


@pytest.fixture
def yahoo_api():
    return YahooAPI()


@pytest.mark.asyncio
async def test_yahoo_fetch_article_success(yahoo_api):
    """
    fetch_articleメソッドの正常テスト
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <li class="newsFeed_item">
                    <a  href="https://news.yahoo.co.jp/articles/sample"></a>
                    <time class="sc-1hy2mez-3 gNVspC">8/16(金) 15:01</time>
                </li>
                <li class="newsFeed_item">
                    <a  href="https://news.yahoo.co.jp/articles/sample"></a>
                    <time class="sc-1hy2mez-3 gNVspC">8/16 15:01</time>
                </li>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.yahoo.co.jp/ranking/access/news/it-science", body=sample_html)
        # テスト
        response = await yahoo_api.fetch_article()
    assert response == {
        "articles": [
            {"url": "https://news.yahoo.co.jp/articles/sample", "published_at": "2024-08-16 15:01:00.000000 +0900"},
            {"url": "https://news.yahoo.co.jp/articles/sample", "published_at": "2024-08-16 15:01:00.000000 +0900"},
        ]
    }


@pytest.mark.asyncio
async def test_yahoo_fetch_article_no_time_tag_skip(yahoo_api):
    """
    fetch_articleメソッドのtimeタグがない場合スキップ
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <li class="newsFeed_item">
                    <a  href="https://news.yahoo.co.jp/articles/sample"></a>
                    <time class="sc-1hy2mez-3 gNVspC">8/16(金) 15:01</time>
                </li>
                <li class="newsFeed_item">
                    <a  href="https://news.yahoo.co.jp/articles/sample"></a>
                </li>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.yahoo.co.jp/ranking/access/news/it-science", body=sample_html)
        # テスト
        response = await yahoo_api.fetch_article()
    assert response == {
        "articles": [
            {"url": "https://news.yahoo.co.jp/articles/sample", "published_at": "2024-08-16 15:01:00.000000 +0900"},
        ]
    }


@pytest.mark.asyncio
async def test_yahoo_fetch_article_no_li_tag_skip(yahoo_api):
    """
    fetch_articleメソッドのliタグがない場合ValueError
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
            <h1>aiu</h1>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.yahoo.co.jp/ranking/access/news/it-science", body=sample_html)
        # テスト
        with pytest.raises(ValueError, match="データまたはarticlesデータの中身が空です"):
            await yahoo_api.fetch_article()


@pytest.mark.asyncio
async def test_yahoo_fetch_article_no_a_tag_skip(yahoo_api):
    """
    fetch_articleメソッドのaタグがない場合ValueError
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <li class="newsFeed_item">
                    <time class="sc-1hy2mez-3 gNVspC">8/16(金) 15:01</time>
                </li>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.yahoo.co.jp/ranking/access/news/it-science", body=sample_html)
        # テスト
        with pytest.raises(ValueError, match="a_tagがありません"):
            await yahoo_api.fetch_article()


@pytest.mark.asyncio
async def test_yahoo_fetch_article_exception(yahoo_api):
    """
    fetch_articleメソッドの例外発生時のテスト
    """
    # requests.getをモック(例外発生)
    with aioresponses() as m:
        m.get("https://news.yahoo.co.jp/ranking/access/news/it-science", exception=aiohttp.ClientError())

        # テスト
        with pytest.raises(aiohttp.ClientError):
            await yahoo_api.fetch_article()


@pytest.mark.asyncio
async def test_fetch_article_title_and_image_success(yahoo_api):
    """
    fetch_article_title_and_imageメソッドの正常テスト
    """
    # サンプルURLを用意
    sample_url = "https://yahoo.com/test/items/test"
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <head>
                <meta property="og:image" content="test_content">
            </head>
            <article>
                <header>
                    <h1>test title</h1>
                </header>
            </article>
        </html>
        """

    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get(sample_url, body=sample_html)
        # テスト
        response = await yahoo_api.fetch_article_title_and_image(sample_url)
    assert response == {"title": "test title", "image_url": "test_content"}


@pytest.mark.asyncio
async def test_fetch_article_title_and_image_no_meta_tag(yahoo_api):
    """
    fetch_article_title_and_imageメソッドのmetaタグがない場合の正常テスト
    """
    # サンプルURLを用意
    sample_url = "https://yahoo.com/test/items/test"
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <head>
                <metas property="og:image" content="test_content">
            </head>
            <article>
                <header>
                    <h1>test title</h1>
                </header>
            </article>
        </html>
        """

    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get(sample_url, body=sample_html)
        # テスト
        response = await yahoo_api.fetch_article_title_and_image(sample_url)
    assert response == {"title": "test title", "image_url": None}


@pytest.mark.asyncio
async def test_fetch_article_title_and_image_no_title_element(yahoo_api):
    """
    fetch_article_title_and_imageメソッドのtitle_elementがない場合の異常テスト
    """
    # サンプルURLを用意
    sample_url = "https://yahoo.com/test/items/test"
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <head>
                <metas property="og:image" content="test_content">
            </head>
            <article>
            </article>
        </html>
        """

    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get(sample_url, body=sample_html)
        # テスト
        with pytest.raises(ValueError, match="title_elementデータの中身が空です"):
            await yahoo_api.fetch_article_title_and_image(sample_url)


@pytest.mark.asyncio
async def test_fetch_article_title_and_image_exception(yahoo_api):
    """
    fetch_article_title_and_imageメソッドの例外発生時のテスト
    """
    sample_url = "https://yahoo.com/test/items/test"

    with aioresponses() as m:
        m.get(sample_url, exception=aiohttp.ClientError())
        # テスト
        with pytest.raises(aiohttp.ClientError):
            await yahoo_api.fetch_article_title_and_image(sample_url)
