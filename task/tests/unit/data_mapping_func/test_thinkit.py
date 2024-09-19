from uuid import uuid4

import pytest
from app.services.data_mapping import thinkit_data_mapping


@pytest.mark.asyncio
async def test_data_mapping_thinkit(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {"title": "Test Article 1", "url": "http://test1.com"}

    ranking = 1
    mock_image = "https://test_image"

    mocker.patch("utils.thinkit.ThinkitAPI.fetch_article_image", return_value=mock_image)

    mapped_data = await thinkit_data_mapping(site_id, article_data_dict, ranking)

    # 値を検証
    assert mapped_data["title"] == article_data_dict["title"]
    assert mapped_data["ranking"] == ranking
    assert mapped_data["url"] == f"https://thinkit.co.jp{article_data_dict["url"]}"
    assert mapped_data["image_url"] == mock_image


# linkが空の場合
@pytest.mark.asyncio
async def test_data_mapping_thinkit_empty_url(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {"title": "Test Article 1", "url": ""}
    ranking = 1

    mapped_data = await thinkit_data_mapping(site_id, article_data_dict, ranking)

    # データをチェック
    assert "image_url" not in mapped_data
