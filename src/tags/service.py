from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.service import BookService
from src.db.models import Tag

from .schemas import TagAddModel, TagCreateModel
from src.errors import BookNotFound, TagNotFound, TagAlreadyExists

bookService = BookService()


serverError = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong"
)


class TagService:

    async def getTags(self, session: AsyncSession):

        statement = select(Tag).order_by(desc(Tag.created_at))

        result = await session.exec(statement)

        return result.all()

    async def addTagsToBook(
        self, bookUid: str, tagData: TagAddModel, session: AsyncSession
    ):

        book = await bookService.getBook(bookUid=bookUid, session=session)

        if not book:
            raise BookNotFound()

        for tagItem in tagData.tags:
            result = await session.exec(select(Tag).where(Tag.name == tagItem.name))

            tag = result.one_or_none()
            if not tag:
                tag = Tag(name=tagItem.name)

            book.tags.append(tag)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def getTagByUid(self, tagUid: str, session: AsyncSession):

        statement = select(Tag).where(Tag.uid == tagUid)

        result = await session.exec(statement)

        return result.first()

    async def addTag(self, tagData: TagCreateModel, session: AsyncSession):

        statement = select(Tag).where(Tag.name == tagData.name)

        result = await session.exec(statement)

        tag = result.first()

        if tag:
            raise TagAlreadyExists()
        newTag = Tag(name=tagData.name)

        session.add(newTag)

        await session.commit()

        return newTag

    async def updateTag(
        self, tagUid, tagUpdateData: TagCreateModel, session: AsyncSession
    ):

        tag = await self.getTagByUid(tagUid, session)

        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        updateDataDict = tagUpdateData.model_dump()

        for k, v in updateDataDict.items():
            setattr(tag, k, v)

            await session.commit()

            await session.refresh(tag)

        return tag

    async def deleteTag(self, tagUid: str, session: AsyncSession):

        tag = self.getTagByUid(tagUid,session)

        if not tag:
            raise TagNotFound()

        await session.delete(tag)

        await session.commit()
    