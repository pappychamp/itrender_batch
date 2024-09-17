from uuid import uuid4

import pytest
from app.services.data_mapping import data_mapping


@pytest.mark.asyncio
async def test_data_mapping(mocker):
    # テスト用の入力データ
    site_id = uuid4()
    article_data_list = [
        {"title": "Test Article 1", "url": "http://test1.com"},
        {"title": "Test Article 2", "url": "http://test2.com"},
    ]

    # モック関数を定義
    async def mock_data_mapping_func(site_id, data, index):
        return {"site_id": site_id, "title": data["title"], "ranking": index}

    # data_mapping_funcにmock_data_mapping_funcを使用
    mapped_data = await data_mapping(site_id, article_data_list, mock_data_mapping_func)

    # データをチェック
    print(locals()["mock_data_mapping_func"])
    assert len(mapped_data) == 2


@pytest.mark.asyncio
async def test_data_mapping_exception():
    site_id = uuid4()
    faulty_data_list = [{"titles": "Test Article 1", "url": "http://test1.com"}]

    # モック関数を定義
    async def mock_data_mapping_func(site_id, data, index):
        return {"site_id": site_id, "title": data["title"], "ranking": index}

    with pytest.raises(Exception):
        await data_mapping(site_id, faulty_data_list, mock_data_mapping_func)
