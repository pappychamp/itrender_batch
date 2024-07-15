import aiohttp
import pytest
from aioresponses import aioresponses
from app.utils.zenn import ZennAPI


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
