import pytest
from app.utils.youtube import YoutubeAPI


@pytest.fixture
def youtube_api():
    return YoutubeAPI()


@pytest.mark.asyncio
async def test_youtube_fetch_video_success(mocker, youtube_api):
    """
    fetch_videoメソッドの正常テスト
    """
    # 仮の返り値
    mock_response = {
        "items": [
            {
                "id": "test_id",
                "snippet": {"title": "Example Video"},
                "player": {},
            },
        ],
    }

    # 仮の関数の振る舞い
    async def mock_execute(*args, **kwargs):
        return mock_response

    # aiogoogle.Aiogoogle.as_api_keyのモック
    mocker.patch("aiogoogle.Aiogoogle.as_api_key", side_effect=mock_execute)

    # テスト
    response = await youtube_api.fetch_video()
    assert response == mock_response


@pytest.mark.asyncio
async def test_youtube_fetch_video_exception(mocker, youtube_api):
    """
    fetch_videoメソッドの例外発生時のテスト
    """

    # 仮の関数の振る舞い
    async def mock_execute(*args, **kwargs):
        raise Exception("Network Error")

    # aiogoogle.Aiogoogle.as_api_keyのモック
    mocker.patch("aiogoogle.Aiogoogle.as_api_key", side_effect=mock_execute)

    # テスト
    with pytest.raises(Exception) as exc_info:
        await youtube_api.fetch_video()
    assert str(exc_info.value) == "Network Error"
