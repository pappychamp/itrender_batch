# from asyncio import current_task

# import pytest

# # from app.db.models import Tag
# from app.db.setting import Base

# # from app.services.db_service import get_or_create_tag
# from sqlalchemy.ext.asyncio import (
#     AsyncSession,
#     async_scoped_session,
#     create_async_engine,
# )

# # from sqlalchemy.future import select
# from sqlalchemy.orm import sessionmaker

# DB_URL = "postgresql+psycopg://postgres:postgres@db:5432/db-test"
# Engine = create_async_engine(DB_URL, echo=False)
# Session = async_scoped_session(
#     sessionmaker(
#         autocommit=False,
#         autoflush=False,
#         bind=Engine,
#         class_=AsyncSession,
#         expire_on_commit=False,
#     ),
#     scopefunc=current_task,
# )


# # テスト用のデータベースとテーブルを作成
# @pytest.fixture(scope="module", autouse=True)
# async def setup_database():
#     async with Engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with Engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# # 非同期セッションを提供するフィクスチャ
# @pytest.fixture
# async def db_session():
#     async with Session() as session:
#         yield session
#         await session.rollback()  # テスト後にロールバックしてクリーンな状態を維持


# @pytest.mark.asyncio
# async def test_get_or_create_tag_existing_tag(db_session):
#     # 既存のタグを作成
#     existing_tag = Tag(name="existing_tag")
#     print("#####")
#     print(db_session)
#     db_session.add(existing_tag)
#     await db_session.commit()


# # 既存のタグを取得
# tag = await get_or_create_tag(async_db_session, "existing_tag")
# assert tag.id == existing_tag.id
# assert tag.name == "existing_tag"


# @pytest.mark.asyncio
# async def test_get_or_create_tag_new_tag(async_db_session):
#     # 新しいタグを作成
#     tag = await get_or_create_tag(async_db_session, "new_tag")
#     assert tag.name == "new_tag"

#     # 新しいタグがデータベースに保存されたか確認
#     result = await async_db_session.execute(select(Tag).filter_by(name="new_tag"))
#     fetched_tag = result.scalars().first()
#     assert fetched_tag is not None
#     assert fetched_tag.name == "new_tag"
