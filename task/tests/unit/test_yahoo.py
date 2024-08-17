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
                <a class="newsFeed_item_link" href="https://news.yahoo.co.jp/articles/sample">
                    <time class="sc-1hy2mez-3 gNVspC">8/16(金) 15:01</time>
                    <div class="newsFeed_item_title">サンプル記事タイトル0</div>
                </a>
                <a class="newsFeed_item_link" href="https://news.yahoo.co.jp/articles/sample">
                    <time class="sc-1hy2mez-3 gNVspC">8/16 15:01</time>
                    <div class="newsFeed_item_title">サンプル記事タイトル1　aa</div>
                </a>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.yahoo.co.jp/ranking/access/news", body=sample_html)
        # テスト
        response = await yahoo_api.fetch_article()
    assert response == {
        "articles": [
            {"title": "サンプル記事タイトル0", "url": "https://news.yahoo.co.jp/articles/sample", "published_at": "2024-08-16 15:01:00.000000 +0900"},
            {"title": "サンプル記事タイトル1 aa", "url": "https://news.yahoo.co.jp/articles/sample", "published_at": "2024-08-16 15:01:00.000000 +0900"},
        ]
    }


@pytest.mark.asyncio
async def test_yahoo_fetch_article_no_newsFeed_item_title_class_skip(yahoo_api):
    """
    fetch_articleメソッドのnewsFeed_item_titleがない場合スキップ
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <a class="newsFeed_item_link" href="https://news.yahoo.co.jp/articles/sample">
                    <time class="sc-1hy2mez-3 gNVspC">8/16(金) 15:01</time>
                    <div class="newsFeed_item_title">サンプル記事タイトル0</div>
                </a>
                <a class="newsFeed_item_link" href="https://news.yahoo.co.jp/articles/sample">
                    <time class="sc-1hy2mez-3 gNVspC">8/16(金) 15:01</time>
                    <div>サンプル記事タイトル1</div>
                </a>
                <a class="newsFeed_item_link" href="https://news.yahoo.co.jp/articles/sample">
                    <time class="sc-1hy2mez-3 gNVspC">8/16(金) 15:01</time>
                    <div class="newsFeed_item_title">サンプル記事タイトル2</div>
                </a>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.yahoo.co.jp/ranking/access/news", body=sample_html)
        # テスト
        response = await yahoo_api.fetch_article()
    assert response == {
        "articles": [
            {"title": "サンプル記事タイトル0", "url": "https://news.yahoo.co.jp/articles/sample", "published_at": "2024-08-16 15:01:00.000000 +0900"},
            {"title": "サンプル記事タイトル2", "url": "https://news.yahoo.co.jp/articles/sample", "published_at": "2024-08-16 15:01:00.000000 +0900"},
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
                <a class="newsFeed_item_link" href="https://news.yahoo.co.jp/articles/sample">
                    <time class="sc-1hy2mez-3 gNVspC">8/16(金) 15:01</time>
                    <div class="newsFeed_item_title">サンプル記事タイトル0</div>
                </a>
                <a class="newsFeed_item_link" href="https://news.yahoo.co.jp/articles/sample">
                    <div class="newsFeed_item_title">サンプル記事タイトル1</div>
                </a>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.yahoo.co.jp/ranking/access/news", body=sample_html)
        # テスト
        response = await yahoo_api.fetch_article()
    assert response == {
        "articles": [
            {"title": "サンプル記事タイトル0", "url": "https://news.yahoo.co.jp/articles/sample", "published_at": "2024-08-16 15:01:00.000000 +0900"},
        ]
    }


@pytest.mark.asyncio
async def test_yahoo_fetch_article_no_a_tag_skip(yahoo_api):
    """
    fetch_articleメソッドのtimeタグがない場合スキップ
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
        m.get("https://news.yahoo.co.jp/ranking/access/news", body=sample_html)
        # テスト
        with pytest.raises(ValueError, match="データまたはarticlesデータの中身が空です"):
            await yahoo_api.fetch_article()


@pytest.mark.asyncio
async def test_yahoo_fetch_article_exception(yahoo_api):
    """
    fetch_articleメソッドの例外発生時のテスト
    """
    # requests.getをモック(例外発生)
    with aioresponses() as m:
        m.get("https://news.yahoo.co.jp/ranking/access/news", exception=aiohttp.ClientError())

        # テスト
        with pytest.raises(aiohttp.ClientError):
            await yahoo_api.fetch_article()
