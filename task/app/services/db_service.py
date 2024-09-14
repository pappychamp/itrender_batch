from db.models import Site, Tag, TrendData
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


async def get_or_create_tag(db_session, tag_name):
    tag_instance = await db_session.execute(select(Tag).filter_by(name=tag_name))
    tag_instance = tag_instance.scalars().first()
    if not tag_instance:
        tag_instance = Tag(name=tag_name)
        db_session.add(tag_instance)
        await db_session.flush()
    return tag_instance


async def create_trend_data(db_session, trend_data_list):
    try:
        new_trends = []
        for trend_data in trend_data_list:
            new_data = TrendData(
                site_id=trend_data["site_id"],
                title=trend_data["title"],
                ranking=trend_data["ranking"],
                published_at=trend_data.get("published_at"),
                category=trend_data.get("category"),
                url=trend_data.get("url"),
                embed_html=trend_data.get("embed_html"),
            )
            # db_session.add(new_data)
            # await db_session.flush()
            tag_instances = []
            for tag in trend_data.get("tags"):
                tag_instance = await get_or_create_tag(db_session, tag.get("name"))
                tag_instances.append(tag_instance)
                new_data.tags.append(tag_instance)
            new_trends.append(new_data)
        db_session.add_all(new_trends)
        await db_session.commit()
        for new_data in new_trends:
            await db_session.refresh(new_data)
        return {"status": "success"}
    except SQLAlchemyError:
        await db_session.rollback()
        raise
    except Exception:
        await db_session.rollback()
        raise


async def get_site_id(db_session, site_name):
    try:
        site_instance = await db_session.execute(select(Site.id).filter_by(name=site_name))
        site_id = site_instance.scalar()
        return site_id
    except Exception:
        raise


# async def main():
#     try:
#         async with Session() as session:
#             print(session)
#             site_id = await get_site_id(session, "youtube")
#             sample_data = [
#                 {
#                     "site_id": site_id,
#                     "title": "test",
#                     # "category": "",
#                     "published_at": parser.parse("2024-06-28T12:00:27Z"),
#                     "url": "",
#                     # "embed_html": None,
#                     "tags": [{"name": "test1"}, {"name": "test2"}],
#                 },
#                 {
#                     "site_id": site_id,
#                     "title": "test2",
#                     # "category": "",
#                     "published_at": parser.parse("2024-06-28T12:00:27Z"),
#                     "url": "",
#                     # "embed_html": None,
#                     "tags": [{"name": "test2"}, {"name": "test3"}],
#                 },
#                 {
#                     "site_id": site_id,
#                     "title": "test3",
#                     # "category": "",
#                     "published_at": parser.parse("2024-06-28T12:00:27Z"),
#                     "url": "",
#                     # "embed_html": None,
#                     # "tags": [{"name": "test2"}, {"name": "test3"}],
#                 },
#             ]
#             valid_data = [TrendDataModel(**data).model_dump() for data in sample_data]
#             res = await create_trend_data(session, valid_data)
#             print(res)
#             # await create_trend_data(
#             #     session,
#             #     site_id,
#             #     "test",
#             #     parser.parse("2024-06-28T12:00:27Z"),
#             #     "music",
#             #     "https://test.com",
#             #     "<h1>",
#             #     ["Python", "自動化"],
#             # )
#     except Exception as e:
#         print("##########")
#         print(e)
#         print("##########")


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())
