import json
import uuid
from datetime import datetime

import pytz
from db.setting import Base, Session
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


# Siteモデル
class Site(Base):
    __tablename__ = "sites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)

    trend_data = relationship("TrendData", back_populates="site")

    def __repr__(self):
        return f"<Site(name={self.name})>"


# 中間テーブル
tag_trend_data = Table(
    "tagtrenddata",
    Base.metadata,
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
    Column("trend_id", UUID(as_uuid=True), ForeignKey("trenddata.id"), primary_key=True),
)


# Tagモデル
class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), nullable=False)

    # trend_data = relationship("TrendData", secondary=tag_trend_data, back_populates="tags")

    def __repr__(self):
        return f"<Tag(name={self.name})>"


# TrendDataモデル
class TrendData(Base):
    __tablename__ = "trenddata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    title = Column(String(255), nullable=False)
    ranking = Column(Integer, nullable=False)
    category = Column(String(255), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    url = Column(String(255), nullable=True)
    embed_html = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone("Asia/Tokyo")), nullable=False)

    site = relationship("Site", back_populates="trend_data")
    tags = relationship(
        "Tag",
        secondary=tag_trend_data,
        # back_populates="trend_data",
    )

    def __repr__(self):
        return f"<TrendData(title={self.title})>"


async def load_initial_data(session):
    with open("/workspace/task/app/db/site_init.json", "r") as file:
        sites_data = json.load(file)

    for site_data in sites_data:
        site = Site(name=site_data["name"], content=site_data["content"])
        session.add(site)

    await session.commit()


# Main script
async def async_main():
    # async with Engine.begin() as conn:
    # Create tables
    # await conn.run_sync(Base.metadata.create_all)

    async with Session() as session:
        await load_initial_data(session)


if __name__ == "__main__":
    import asyncio

    asyncio.run(async_main())
