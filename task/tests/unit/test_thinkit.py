import aiohttp
import pytest
from aioresponses import aioresponses
from app.utils.thinkit import ThinkitAPI


@pytest.fixture
def thinkit_api():
    return ThinkitAPI()


@pytest.mark.asyncio
async def test_thinkit_fetch_article_success(thinkit_api):
    """
    fetch_articleメソッドの正常テスト
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <div class="views-field views-field-title">        
                    <span class="field-content">
                        <a href="/test/0">サンプル記事タイトル0</a>
                    </span>  
                </div>
                <div class="views-field views-field-title">        
                    <span class="field-content">
                        <a href="/test/1">サンプル記事タイトル1　aa</a>
                    </span>  
                </div>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://thinkit.co.jp/ranking/daily", body=sample_html)
        # テスト
        response = await thinkit_api.fetch_article()
    assert response == {
        "articles": [
            {"title": "サンプル記事タイトル0", "url": "/test/0"},
            {"title": "サンプル記事タイトル1 aa", "url": "/test/1"},
        ]
    }


@pytest.mark.asyncio
async def test_thinkit_fetch_article_no_newsFeed_item_title_class_skip(thinkit_api):
    """
    fetch_articleメソッドのaタグがない場合がない場合スキップ
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <div class="views-field views-field-title">        
                    <span class="field-content">
                        <a href="/test/0">サンプル記事タイトル0</a>
                    </span>  
                </div>
                <div class="views-field views-field-title">        
                    <span class="field-content">
                        <h1 href="/test/1">サンプル記事タイトル1</h1>
                    </span>  
                </div>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://thinkit.co.jp/ranking/daily", body=sample_html)
        # テスト
        response = await thinkit_api.fetch_article()
    assert response == {
        "articles": [
            {"title": "サンプル記事タイトル0", "url": "/test/0"},
        ]
    }


@pytest.mark.asyncio
async def test_thinkit_fetch_article_no_a_tag_skip(thinkit_api):
    """
    fetch_articleメソッドのdivタグでviews-field views-field-titleクラスがない場合ValueError
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <body>
                <div class="views-field">        
                    <span class="field-content">
                        <h1 href="/test/1">サンプル記事タイトル1</h1>
                    </span>  
                </div>
            </body>
        </html>
        """
    with aioresponses() as m:
        # payloadはJSONデータを返すときに使用するものでありHTMLコンテンツを返すにはbodyを使う必要がある
        m.get("https://thinkit.co.jp/ranking/daily", body=sample_html)
        # テスト
        with pytest.raises(ValueError, match="データまたはarticlesデータの中身が空です"):
            await thinkit_api.fetch_article()


@pytest.mark.asyncio
async def test_thinkit_fetch_article_exception(thinkit_api):
    """
    fetch_articleメソッドの例外発生時のテスト
    """
    # requests.getをモック(例外発生)
    with aioresponses() as m:
        m.get("https://thinkit.co.jp/ranking/daily", exception=aiohttp.ClientError())

        # テスト
        with pytest.raises(aiohttp.ClientError):
            await thinkit_api.fetch_article()
