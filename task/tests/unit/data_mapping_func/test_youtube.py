from uuid import uuid4

import pytest
from app.services.data_mapping import youtube_data_mapping
from dateutil import parser


@pytest.mark.asyncio
async def test_data_mapping_youtube(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {
        "id": "test_id_1",
        "snippet": {
            "categoryId": "123",
            "title": "Test Video 1",
            "tags": ["tag1", "tag2"],
            "publishedAt": "2024-07-15T12:00:00Z",
            "thumbnails": {
                "standard": {"url": "https://i.ytimg.com/vi/n0uXxGSYYL0/sddefault.jpg", "width": 640, "height": 480},
            },
        },
        "player": {"embedHtml": "<iframe></iframe>"},
    }

    ranking = 1

    mapped_data = await youtube_data_mapping(site_id, article_data_dict, ranking)

    # 値を検証
    assert mapped_data["title"] == article_data_dict["snippet"]["title"]
    assert mapped_data["ranking"] == ranking
    assert mapped_data["url"] == f"https://www.youtube.com/watch?v={article_data_dict["id"]}"
    assert mapped_data["published_at"] == parser.parse(article_data_dict["snippet"]["publishedAt"])
    assert mapped_data["embed_html"] == article_data_dict["player"]["embedHtml"]
    assert mapped_data["image_url"] == article_data_dict["snippet"]["thumbnails"]["standard"]["url"]
    assert mapped_data["category"] == article_data_dict["snippet"]["categoryId"]
    assert sorted(mapped_data["tags"], key=lambda x: x["name"]) == sorted([{"name": tag} for tag in article_data_dict["snippet"]["tags"]], key=lambda x: x["name"])


# thumbnailsがない場合
@pytest.mark.asyncio
async def test_data_mapping_youtube_no_thumbnails(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_dict = {
        "id": "test_id_1",
        "snippet": {
            "categoryId": "123",
            "title": "Test Video 1",
            "tags": ["tag1", "tag2"],
            "publishedAt": "2024-07-15T12:00:00Z",
        },
        "player": {"embedHtml": "<iframe></iframe>"},
    }

    ranking = 1

    mapped_data = await youtube_data_mapping(site_id, article_data_dict, ranking)

    # 値を検証
    assert mapped_data["image_url"] is None


# タグに重複がある場合
@pytest.mark.asyncio
async def test_data_mapping_youtube_duplicate_tag():
    site_id = uuid4()
    article_data_dict = {
        "id": "test_id_1",
        "snippet": {"categoryId": "123", "title": "Test Video 1", "tags": ["tag1", "tag2", "tag2"], "publishedAt": "2024-07-15T12:00:00Z"},
        "player": {"embedHtml": "<iframe></iframe>"},
    }
    ranking = 1

    mapped_data = await youtube_data_mapping(site_id, article_data_dict, ranking)
    # データをチェック
    assert len(mapped_data["tags"]) == 2
