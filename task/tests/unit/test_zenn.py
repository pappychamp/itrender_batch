import aiohttp
import pytest
from aioresponses import aioresponses
from app.utils.zenn import ZennAPI
from bs4 import BeautifulSoup


@pytest.fixture
def zenn_api():
    return ZennAPI()


@pytest.mark.asyncio
async def test_zenn_fetch_article_success(zenn_api):
    """
    fetch_articleメソッドの正常テスト
    """
    # requests.getをモック(payloadが仮の返り値)
    with aioresponses() as m:
        m.get("https://zenn.dev/api/articles", payload={"articles": [{"title": "Article 1"}]})
        # テスト
        response = await zenn_api.fetch_article()
    assert response == {"articles": [{"title": "Article 1"}]}


@pytest.mark.asyncio
async def test_zenn_fetch_article_no_data(zenn_api):
    """
    fetch_articleメソッドのデータの中身が空のテスト
    """
    # requests.getをモック(payloadが仮の返り値)
    with aioresponses() as m:
        m.get("https://zenn.dev/api/articles", payload={})
        # テスト
        with pytest.raises(ValueError, match="データまたはarticlesデータの中身が空です"):
            await zenn_api.fetch_article()


@pytest.mark.asyncio
async def test_zenn_fetch_article_exception(zenn_api):
    """
    fetch_articleメソッドの例外発生時のテスト
    """
    # requests.getをモック(例外発生)
    with aioresponses() as m:
        m.get("https://zenn.dev/api/articles", exception=aiohttp.ClientError())

        # テスト
        with pytest.raises(aiohttp.ClientError):
            await zenn_api.fetch_article()


@pytest.mark.asyncio
async def test_zenn_fetch_article_image_success(zenn_api):
    """
    fetch_article_imageメソッドの正常テスト
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <head>
                <meta property="og:image" content="test_content">
            </head>
        </html>
        """
    soup = BeautifulSoup(sample_html, "html.parser")
    # テスト
    result = await zenn_api.fetch_article_image(soup)
    assert result == "test_content"


@pytest.mark.asyncio
async def test_zenn_fetch_article_image_no_a_tag(zenn_api):
    """
    fetch_article_imageメソッドのmetaタグがない場合の正常テスト
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <head>
                <metas property="og:image" content="test_content">
            </head>
        </html>
        """
    soup = BeautifulSoup(sample_html, "html.parser")
    # テスト
    result = await zenn_api.fetch_article_image(soup)
    assert result is None


@pytest.mark.asyncio
async def test_zenn_fetch_article_image_exception(zenn_api):
    """
    fetch_article_imageメソッドの例外発生時のテスト
    """
    soup = None

    # pytest.raisesを使って例外が発生するかを確認
    with pytest.raises(Exception):
        await zenn_api.fetch_article_image(soup)


@pytest.mark.asyncio
async def test_zenn_fetch_article_tag_success(zenn_api):
    """
    fetch_article_tagメソッドの正常テスト
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <div class="View_topicName__test">
                test_tag
            </div>
        </html>
        """
    soup = BeautifulSoup(sample_html, "html.parser")
    # テスト
    result = await zenn_api.fetch_article_tag(soup)
    assert result == ["test_tag"]


@pytest.mark.asyncio
async def test_zenn_fetch_article_tag_no_a_tag(zenn_api):
    """
    fetch_article_tagメソッドのmetaタグがない場合の正常テスト
    """
    # サンプルHTMLを用意
    sample_html = """
        <html>
            <div class="test_View_topicName__test">
                test_tag
            </div>
        </html>
        """
    soup = BeautifulSoup(sample_html, "html.parser")
    # テスト
    result = await zenn_api.fetch_article_tag(soup)
    assert result == []


@pytest.mark.asyncio
async def test_zenn_fetch_article_tag_exception(zenn_api):
    """
    fetch_article_tagメソッドの例外発生時のテスト
    """
    soup = None

    # pytest.raisesを使って例外が発生するかを確認
    with pytest.raises(Exception):
        await zenn_api.fetch_article_tag(soup)
