from datetime import datetime
from uuid import uuid4

import pytest
from app.services.data_validate import TrendDataModel
from pydantic import ValidationError


# 正常系
def test_valid_trend_data_model():
    data = {
        "site_id": uuid4(),
        "title": "Test Title",
        "ranking": 1,
        "category": "Test Category",
        "published_at": datetime.now(),
        "url": "https://example.com",
        "embed_html": "<div>Embed HTML</div>",
        "tags": [{"name": "test"}],
    }
    model = TrendDataModel(**data)
    assert model.site_id == data["site_id"]
    assert model.ranking == data["ranking"]
    assert model.title == data["title"]
    assert model.category == data["category"]
    assert model.published_at == data["published_at"]
    assert model.url == data["url"]
    assert model.embed_html == data["embed_html"]
    assert model.tags[0].name == "test"


def test_trend_data_model_empty_tags():
    # tagsが空リスト
    data = {
        "site_id": uuid4(),
        "title": "Test Title",
        "ranking": 1,
        "category": "Test Category",
        "published_at": datetime.now(),
        "url": "https://example.com",
        "embed_html": "<div>Embed HTML</div>",
        "tags": [],  # 空のtagsリスト
    }
    model = TrendDataModel(**data)
    assert model.tags == []


def test_trend_data_model_no_tags():
    # tagsフィールドがない
    data = {
        "site_id": uuid4(),
        "title": "Test Title",
        "ranking": 1,
        "category": "Test Category",
        "published_at": datetime.now(),
        "url": "https://example.com",
        "embed_html": "<div>Embed HTML</div>",
    }
    model = TrendDataModel(**data)
    assert model.tags == []


def test_trend_data_model_no_field():
    # category,published_at,url,embed_htmlフィールドがない
    data = {
        "site_id": uuid4(),
        "title": "Test Title",
        "ranking": 1,
        "tags": [],  # 空のtagsリスト
    }
    model = TrendDataModel(**data)
    assert model.category is None
    assert model.published_at is None
    assert model.url is None
    assert model.embed_html is None


def test_trend_data_model_empty_field():
    # category,url,embed_htmlが空
    data = {
        "site_id": uuid4(),
        "title": "Test Title",
        "ranking": 1,
        "category": "",
        "url": "",
        "embed_html": "",
        "tags": [],  # 空のtagsリスト
    }
    model = TrendDataModel(**data)
    assert model.category == ""
    assert model.url == ""
    assert model.embed_html == ""


def test_trend_data_model_none_field():
    # category,url,embed_htmlがNone
    data = {
        "site_id": uuid4(),
        "title": "Test Title",
        "ranking": 1,
        "category": None,
        "url": None,
        "embed_html": None,
        "tags": [],  # 空のtagsリスト
    }
    model = TrendDataModel(**data)
    assert model.category is None
    assert model.url is None
    assert model.embed_html is None


# 異常系
def test_invalid_trend_data_model():
    # タイトルがNoneの場合
    with pytest.raises(ValidationError) as excinfo:
        TrendDataModel(
            site_id=uuid4(),
            title=None,
            ranking=1,
            category="Test Category",
            published_at=datetime.now(),
            url="https://example.com",
            embed_html="<div>Embed HTML</div>",
            tags=[{"name": "test"}],
        )
    assert "title" in str(excinfo.value)

    # rankingがNoneの場合
    with pytest.raises(ValidationError) as excinfo:
        TrendDataModel(
            site_id=uuid4(),
            title="test",
            ranking=None,
            category="Test Category",
            published_at=datetime.now(),
            url="https://example.com",
            embed_html="<div>Embed HTML</div>",
            tags=[{"name": "test"}],
        )
    assert "ranking" in str(excinfo.value)

    # 無効なUUID
    with pytest.raises(ValidationError) as excinfo:
        TrendDataModel(
            site_id="invalid-uuid",
            title="Test Title",
            ranking=1,
            category="Test Category",
            published_at=datetime.now(),
            url="https://example.com",
            embed_html="<div>Embed HTML</div>",
            tags=[{"name": "test"}],
        )
    assert "site_id" in str(excinfo.value)

    # 発行日が無効な形式
    with pytest.raises(ValidationError) as excinfo:
        TrendDataModel(
            site_id=uuid4(),
            title="Test Title",
            ranking=1,
            category="Test Category",
            published_at="invalid-date",
            url="https://example.com",
            embed_html="<div>Embed HTML</div>",
            tags=[{"name": "test"}],
        )
    assert "published_at" in str(excinfo.value)

    # titleが長さ255以上
    with pytest.raises(ValidationError) as excinfo:
        TrendDataModel(
            site_id=uuid4(),
            title="x" * 256,
            ranking=1,
            category="Test Category",
            published_at=datetime.now(),
            url="https://example.com",
            embed_html="<div>Embed HTML</div>",
            tags=[{"name": "test"}],
        )
    assert "title" in str(excinfo.value)
