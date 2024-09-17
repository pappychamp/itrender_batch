from uuid import uuid4

import pytest
from app.services.data_mapping import qiita_data_mapping
from dateutil import parser


@pytest.mark.asyncio
async def test_data_mapping_qiita(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {
        "title": "Test Article 1",
        "link": "https://test_url",
        "updated": "2024-07-15T12:00:00Z",
        "tags": [{"name": "tag1"}, {"name": "tag2"}],
    }
    ranking = 1
    mock_image = "https://test_image"

    mocker.patch("utils.qiita.QiitaAPI.fetch_article_image", return_value=mock_image)

    mapped_data = await qiita_data_mapping(site_id, article_data_dict, ranking)

    # 値を検証
    assert mapped_data["title"] == article_data_dict["title"]
    assert mapped_data["ranking"] == ranking
    assert mapped_data["tags"] == article_data_dict["tags"]
    assert mapped_data["url"] == article_data_dict["link"]
    assert mapped_data["published_at"] == parser.parse(article_data_dict["updated"])
    assert mapped_data["embed_html"] == mock_image


# linkが空の場合
@pytest.mark.asyncio
async def test_data_mapping_qiita_empty_url(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {"title": "Test Article 1", "link": "", "updated": "2024-07-15T12:00:00Z"}
    ranking = 1

    mapped_data = await qiita_data_mapping(site_id, article_data_dict, ranking)

    # データをチェック
    assert "embed_html" not in mapped_data


# タグに重複がある場合
@pytest.mark.asyncio
async def test_data_mapping_qiita_duplicate_tag():
    site_id = uuid4()
    article_data_dict = {
        "title": "Test Article 1",
        "tags": [{"name": "tag1"}, {"name": "tag2"}, {"name": "tag2"}],
        "updated": "2024-07-15T12:00:00Z",
    }
    ranking = 1

    mapped_data = await qiita_data_mapping(site_id, article_data_dict, ranking)
    # データをチェック
    assert len(mapped_data["tags"]) == 2
