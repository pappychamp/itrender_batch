import pytest
from datetime import datetime
from uuid import uuid4
from pydantic import ValidationError
from services.data_validate import TrendDataModel


def test_valid_trend_data_model():
    data = {
        "site_id": uuid4(),
        "title": "Test Title",
        "category": "Test Category",
        "published_at": datetime.now(),
        "url": "https://example.com",
        "embed_html": "<div>Embed HTML</div>",
        "tags": [{"name": "test"}],
    }
    model = TrendDataModel(**data)
    assert model.site_id == data["site_id"]
    assert model.title == data["title"]
    assert model.category == data["category"]
    assert model.published_at == data["published_at"]
    assert model.url == data["url"]
    assert model.embed_html == data["embed_html"]
    assert model.tags[0].name == "test"


def test_invalid_trend_data_model():
    # タイトルが空の場合
    with pytest.raises(ValidationError) as excinfo:
        TrendDataModel(
            site_id=uuid4(),
            title=None,
            category="Test Category",
            published_at=datetime.now(),
            url="https://example.com",
            embed_html="<div>Embed HTML</div>",
            tags=[{"name": "test"}],
        )
    assert "title" in str(excinfo.value)

    # 無効なUUID
    with pytest.raises(ValidationError) as excinfo:
        TrendDataModel(
            site_id="invalid-uuid",
            title="Test Title",
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
            category="Test Category",
            published_at=datetime.now(),
            url="https://example.com",
            embed_html="<div>Embed HTML</div>",
            tags=[{"name": "test"}],
        )
    assert "title" in str(excinfo.value)

    # titleが長さ255以上
    with pytest.raises(ValidationError) as excinfo:
        TrendDataModel(
            site_id=uuid4(),
            title="x" * 256,
            category="Test Category",
            published_at=datetime.now(),
            url="https://example.com",
            embed_html="<div>Embed HTML</div>",
            tags=[{"name": "test"}],
        )
    assert "title" in str(excinfo.value)
