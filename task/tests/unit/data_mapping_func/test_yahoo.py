from uuid import uuid4

import pytest
from app.services.data_mapping import yahoo_data_mapping
from dateutil import parser


@pytest.mark.asyncio
async def test_data_mapping_yahoo(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {
        "url": "http://test1.com",
        "published_at": "2024-08-16 15:01:00.000000 +0900",
    }

    ranking = 1
    mock_image = {"title": "Test Article 1", "image_url": "https://test_image"}

    mocker.patch("utils.yahoo.YahooAPI.fetch_article_title_and_image", return_value=mock_image)

    mapped_data = await yahoo_data_mapping(site_id, article_data_dict, ranking)

    # 値を検証
    assert mapped_data["title"] == mock_image["title"]
    assert mapped_data["ranking"] == ranking
    assert mapped_data["url"] == article_data_dict["url"]
    assert mapped_data["published_at"] == parser.parse(article_data_dict["published_at"])
    assert mapped_data["image_url"] == mock_image["image_url"]


# linkが空の場合
@pytest.mark.asyncio
async def test_data_mapping_yahoo_empty_url(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {
        "url": "",
        "published_at": "2024-08-16 15:01:00.000000 +0900",
    }
    ranking = 1

    mapped_data = await yahoo_data_mapping(site_id, article_data_dict, ranking)

    # データをチェック
    assert "image_url" not in mapped_data
