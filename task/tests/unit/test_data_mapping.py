from datetime import datetime
from uuid import uuid4

import pytest
from app.services.data_mapping import (
    data_mapping,
    qiita_data_mapping,
    techplus_data_mapping,
    thinkit_data_mapping,
    yahoo_data_mapping,
    youtube_data_mapping,
    zenn_data_mapping,
)
from dateutil import parser


@pytest.mark.asyncio
async def test_data_mapping_zenn():
    # テスト用の入力データ
    site_id = uuid4()
    article_data_list = [
        {"title": "Test Article 1", "path": "/articles/1", "published_at": "2024-07-15T12:00:00Z"},
        {"title": "Test Article 2", "path": "/articles/2", "published_at": "2024-07-16T12:00:00+0900"},
    ]

    # data_mapping_funcにzenn_data_mappingを使用
    mapped_data = await data_mapping(site_id, article_data_list, zenn_data_mapping)

    # データをチェック
    assert len(mapped_data) == 2
    for original, mapped in zip(article_data_list, mapped_data):
        assert "site_id" in mapped
        assert "title" in mapped
        assert "url" in mapped
        assert "published_at" in mapped
        assert "ranking" in mapped
        assert isinstance(mapped["published_at"], datetime)

        # 値を検証
        assert mapped["title"] == original["title"]
        assert mapped["url"] == f"https://zenn.dev{original["path"]}"
        assert mapped["published_at"] == parser.parse(original["published_at"])

@pytest.mark.asyncio
async def test_data_mapping_youtube():
    # テスト用の入力データ
    site_id = uuid4()
    video_data_list = [
        {"id": "test_id_1", "snippet": {"categoryId": "123", "title": "Test Video 1", "tags": ["tag1", "tag2"], "publishedAt": "2024-07-15T12:00:00Z"}, "player": {"embedHtml": "<iframe></iframe>"}},
        {"id": "test_id_2", "snippet": {"categoryId": "456", "title": "Test Video 2", "publishedAt": "2024-07-16T12:00:00Z"}, "player": {"embedHtml": "<iframe></iframe>"}},
    ]

    # data_mapping_funcにyoutube_data_mappingを使用
    mapped_data = await data_mapping(site_id, video_data_list, youtube_data_mapping)

    # データをチェック
    assert len(mapped_data) == 2
    for original, mapped in zip(video_data_list, mapped_data):
        assert "site_id" in mapped
        assert "title" in mapped
        assert isinstance(mapped["tags"], list)
        assert "url" in mapped
        assert "published_at" in mapped
        assert "embed_html" in mapped
        assert "category" in mapped
        assert "ranking" in mapped
        assert isinstance(mapped["published_at"], datetime)

        # 値を検証
        assert mapped["title"] == original["snippet"]["title"]
        assert mapped["url"] == f"https://www.youtube.com/watch?v={original["id"]}"
        assert mapped["published_at"] == parser.parse(original["snippet"]["publishedAt"])
        assert mapped["embed_html"] == original["player"]["embedHtml"]
        assert mapped["category"] == original["snippet"]["categoryId"]


@pytest.mark.asyncio
async def test_data_mapping_qiita():
    # テスト用の入力データ
    site_id = uuid4()
    article_data_list = [
        {"title": "Test Article 1", "tags": [{"name": "tag1", "versions": []}, {"name": "tag2", "versions": []}], "link": "http://test1.com", "updated": "2024-07-15T12:00:00Z"},
        {"title": "Test Article 2", "link": "http://test2.com", "updated": "2024-07-16T12:00:00Z"},
    ]

    # data_mapping_funcにqiita_data_mappingを使用
    mapped_data = await data_mapping(site_id, article_data_list, qiita_data_mapping)
    # データをチェック
    assert len(mapped_data) == 2
    for original, mapped in zip(article_data_list, mapped_data):
        assert "site_id" in mapped
        assert "title" in mapped
        assert "tags" in mapped
        assert "url" in mapped
        assert "published_at" in mapped
        assert "ranking" in mapped
        assert isinstance(mapped["published_at"], datetime)

        # 値を検証
        assert mapped["title"] == original["title"]
        assert mapped["url"] == original["link"]
        assert mapped["published_at"] == parser.parse(original["updated"])

@pytest.mark.asyncio
async def test_data_mapping_yahoo():
    # テスト用の入力データ
    site_id = uuid4()
    article_data_list = [
        {"title": "Test Article 1", "url": "http://test1.com", "published_at": "2024-08-16 15:01:00.000000 +0900"},
        {"title": "Test Article 2", "url": "http://test2.com", "published_at": "2024-08-16 15:01:00.000000 +0900"},
    ]

    # data_mapping_funcにyahoo_data_mappingを使用
    mapped_data = await data_mapping(site_id, article_data_list, yahoo_data_mapping)

    # データをチェック
    assert len(mapped_data) == 2
    for original, mapped in zip(article_data_list, mapped_data):
        assert "site_id" in mapped
        assert "title" in mapped
        assert "url" in mapped
        assert "published_at" in mapped
        assert "ranking" in mapped
        assert isinstance(mapped["published_at"], datetime)

        # 値を検証
        assert mapped["title"] == original["title"]
        assert mapped["url"] == original["url"]
        assert mapped["published_at"] == parser.parse(original["published_at"])


@pytest.mark.asyncio
async def test_data_mapping_thinkit():
    # テスト用の入力データ
    site_id = uuid4()
    article_data_list = [
        {"title": "Test Article 1", "url": "http://test1.com"},
        {"title": "Test Article 2", "url": "http://test2.com"},
    ]

    # data_mapping_funcにthinkit_data_mappingを使用
    mapped_data = await data_mapping(site_id, article_data_list, thinkit_data_mapping)

    # データをチェック
    assert len(mapped_data) == 2
    for original, mapped in zip(article_data_list, mapped_data):
        assert "site_id" in mapped
        assert "title" in mapped
        assert "url" in mapped
        assert "ranking" in mapped

        # 値を検証
        assert mapped["title"] == original["title"]
        assert mapped["url"] == f"https://thinkit.co.jp{original["url"]}"


@pytest.mark.asyncio
async def test_data_mapping_techplus():
    # テスト用の入力データ
    site_id = uuid4()
    article_data_list = [
        {"title": "Test Article 1", "url": "/articles/1"},
        {"title": "Test Article 2", "url": "/articles/2"},
    ]

    # data_mapping_funcにtechplus_data_mappingを使用
    mapped_data = await data_mapping(site_id, article_data_list, techplus_data_mapping)

    # データをチェック
    assert len(mapped_data) == 2
    for original, mapped in zip(article_data_list, mapped_data):
        assert "site_id" in mapped
        assert "title" in mapped
        assert "url" in mapped
        assert "ranking" in mapped

        # 値を検証
        assert mapped["title"] == original["title"]
        assert mapped["url"] == f"https://news.mynavi.jp{original["url"]}"


@pytest.mark.asyncio
async def test_data_mapping_exception():
    site_id = uuid4()
    faulty_data_list = [{"title": "Faulty Article", "path": "/articles/faulty", "published_at": "invalid-date"}]

    with pytest.raises(Exception):
        await data_mapping(site_id, faulty_data_list, zenn_data_mapping)


@pytest.mark.asyncio
async def test_data_mapping_youtube_duplicate_tag():
    # タグに重複があるデータ
    site_id = uuid4()
    video_data_list = [
        {
            "id": "test_id_1",
            "snippet": {"categoryId": "123", "title": "Test Video 1", "tags": ["tag1", "tag2", "tag2"], "publishedAt": "2024-07-15T12:00:00Z"},
            "player": {"embedHtml": "<iframe></iframe>"},
        },
    ]

    # data_mapping_funcにyoutube_data_mappingを使用
    mapped_data = await data_mapping(site_id, video_data_list, youtube_data_mapping)

    # データをチェック
    assert len(mapped_data) == 1
    for data in mapped_data:
        assert len(data.get("tags")) == 2


@pytest.mark.asyncio
async def test_data_mapping_qiita_duplicate_tag():
    # タグに重複があるデータ
    site_id = uuid4()
    article_data_list = [
        {
            "title": "Test Article 1",
            "tags": [{"name": "tag1", "versions": []}, {"name": "tag2", "versions": []}, {"name": "tag2", "versions": []}],
            "link": "/articles/1",
            "updated": "2024-07-15T12:00:00Z",
        }
    ]

    # data_mapping_funcにqiita_data_mappingを使用
    mapped_data = await data_mapping(site_id, article_data_list, qiita_data_mapping)
    # データをチェック
    assert len(mapped_data) == 1
    for data in mapped_data:
        assert len(data.get("tags")) == 2
