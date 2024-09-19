from uuid import uuid4

import pytest
from app.services.data_mapping import zenn_data_mapping
from dateutil import parser


@pytest.mark.asyncio
async def test_data_mapping_zenn(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {"title": "Test Article 1", "path": "/articles/1", "published_at": "2024-07-15T12:00:00Z"}
    ranking = 1
    mock_image_and_tag = {"image_url": "https://test_image", "tags": ["test1", "test2"]}

    mocker.patch("utils.zenn.ZennAPI.fetch_article_image_and_tag", return_value=mock_image_and_tag)

    mapped_data = await zenn_data_mapping(site_id, article_data_dict, ranking)

    # 値を検証
    assert mapped_data["title"] == article_data_dict["title"]
    assert mapped_data["ranking"] == ranking
    assert sorted(mapped_data["tags"], key=lambda x: x["name"]) == sorted([{"name": tag} for tag in mock_image_and_tag["tags"]], key=lambda x: x["name"])
    assert mapped_data["url"] == f"https://zenn.dev{article_data_dict["path"]}"
    assert mapped_data["published_at"] == parser.parse(article_data_dict["published_at"])
    assert mapped_data["image_url"] == "https://test_image"


# pathが空の場合
@pytest.mark.asyncio
async def test_data_mapping_zenn_empty_path(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {"title": "Test Article 1", "path": "", "published_at": "2024-07-15T12:00:00Z"}
    ranking = 1

    # data_mapping_funcにzenn_data_mappingを使用
    mapped_data = await zenn_data_mapping(site_id, article_data_dict, ranking)
    # データをチェック
    assert "image_url" not in mapped_data
    assert "tags" not in mapped_data
