import aiohttp
import pytest
from aioresponses import aioresponses
from app.utils.techplus import TechplusAPI


@pytest.fixture
def techplus_api():
    return TechplusAPI()


@pytest.mark.asyncio
async def test_techplus_fetch_article_success(techplus_api):
    """
    fetch_articleメソッドの正常テスト
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <a class="rankingtList_listNode_link" href="/test/0">
                    <div>
                      <h3 class="rankingtList_listNode_catch">
                        サンプル記事タイトル0
                      </h3>
                    </div>
                </a>
                <a class="rankingtList_listNode_link" href="/test/1">
                    <div>
                      <h3 class="rankingtList_listNode_catch">
                        サンプル記事タイトル1　aa
                      </h3>
                    </div>
                </a>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.mynavi.jp/techplus/ranking/", body=sample_html)
        # テスト
        response = await techplus_api.fetch_article()
    assert response == {
        "articles": [
            {"title": "サンプル記事タイトル0", "url": "/test/0"},
            {"title": "サンプル記事タイトル1 aa", "url": "/test/1"},
        ]
    }


@pytest.mark.asyncio
async def test_techplus_fetch_article_no_newsFeed_item_title_class_skip(techplus_api):
    """
    fetch_articleメソッドのh3タグでankingtList_listNode_catchクラスがない場合がない場合スキップ
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <a class="rankingtList_listNode_link" href="/test/0">
                    <div>
                      <h3 class="rankingtList_listNode_catch">
                        サンプル記事タイトル0
                      </h3>
                    </div>
                </a>
                <a class="rankingtList_listNode_link" href="/test/1">
                    <div>
                      <h3>
                        サンプル記事タイトル1
                      </h3>
                    </div>
                </a>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.mynavi.jp/techplus/ranking/", body=sample_html)
        # テスト
        response = await techplus_api.fetch_article()
    assert response == {
        "articles": [
            {"title": "サンプル記事タイトル0", "url": "/test/0"},
        ]
    }


@pytest.mark.asyncio
async def test_techplus_fetch_article_no_a_tag_skip(techplus_api):
    """
    fetch_articleメソッドのaタグでrankingtList_listNode_linkクラスがない場合ValueError
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <a href="/test/0">
                    <div>
                      <h3 class="rankingtList_listNode_catch">
                        サンプル記事タイトル0
                      </h3>
                    </div>
                </a>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://news.mynavi.jp/techplus/ranking/", body=sample_html)
        # テスト
        with pytest.raises(ValueError, match="データまたはarticlesデータの中身が空です"):
            await techplus_api.fetch_article()


@pytest.mark.asyncio
async def test_techplus_fetch_article_exception(techplus_api):
    """
    fetch_articleメソッドの例外発生時のテスト
    """
    # requests.getをモック(例外発生)
    with aioresponses() as m:
        m.get("https://news.mynavi.jp/techplus/ranking/", exception=aiohttp.ClientError())

        # テスト
        with pytest.raises(aiohttp.ClientError):
            await techplus_api.fetch_article()


@pytest.mark.asyncio
async def test_fetch_article_image_success(techplus_api):
    """
    fetch_article_imageメソッドの正常テスト
    """
    # サンプルURLを用意
    sample_url = "https://techplus.com/test/items/test"
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
        response = await techplus_api.fetch_article_image(sample_url)
    assert response == "test_content"


@pytest.mark.asyncio
async def test_fetch_article_image_no_a_tag(techplus_api):
    """
    fetch_article_imageメソッドのmetaタグがない場合の正常テスト
    """
    # サンプルURLを用意
    sample_url = "https://techplus.com/test/items/test"
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
        response = await techplus_api.fetch_article_image(sample_url)
    assert response is None


@pytest.mark.asyncio
async def test_fetch_article_image_exception(techplus_api):
    """
    fetch_article_imageメソッドの例外発生時のテスト
    """
    sample_url = "https://techplus.com/test/items/test"

    with aioresponses() as m:
        m.get(sample_url, exception=aiohttp.ClientError())
        # テスト
        with pytest.raises(aiohttp.ClientError):
            await techplus_api.fetch_article_image(sample_url)
