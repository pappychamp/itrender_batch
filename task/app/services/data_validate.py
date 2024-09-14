import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SiteModel(BaseModel):
    name: str = Field(..., min_length=1, description="SiteName cannot be empty")
    content: str = Field(..., min_length=1, description="Content cannot be empty")


class TagModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="TagName cannot be empty")


class TrendDataModel(BaseModel):
    site_id: uuid.UUID
    title: str = Field(..., min_length=1, max_length=255, description="Title cannot be empty")
    ranking: int = Field(None, description="Ranking of the item")
    category: Optional[str] = Field(None, max_length=255, description="Category must be a string with a maximum length of 255 characters")
    published_at: Optional[datetime]
    url: Optional[str] = Field(None, max_length=255, description="URL must be a string with a maximum length of 255 characters")
    embed_html: Optional[str] = Field(None, description="EmbedHtml must be a string")
    tags: List[TagModel] | None = []

    # @field_validator("title")
    # def title_must_not_be_empty(cls, v):
    #     if not v.strip():
    #         raise ValueError("Title cannot be empty")
    #     return v

    # @field_validator("published_at")
    # def published_at_must_be_in_past(cls, v):
    #     if v > datetime.now():
    #         raise ValueError("Published date cannot be in the future")
    #     return v
