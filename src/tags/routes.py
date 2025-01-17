from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession


from src.auth.dependencies import RoleChecker
from src.books.schemas import BookModel
from src.db.main import getSession

from .schemas import TagAddModel, TagCreateModel, TagModel
from .service import TagService

tagsRouter = APIRouter()
tagService = TagService()
userRoleChecker = Depends(RoleChecker(["user", "admin"]))


@tagsRouter.get("/", response_model=List[TagModel], dependencies=[userRoleChecker])
async def getAllTags(session: AsyncSession = Depends(getSession)):
    tags = await tagService.getTags(session)

    return tags


@tagsRouter.post(
    "/",
    response_model=TagModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[userRoleChecker],
)
async def addTag(
    tagData: TagCreateModel, session: AsyncSession = Depends(getSession)
) -> TagModel:

    tagAdded = await tagService.addTag(tagData=tagData, session=session)

    return tagAdded


@tagsRouter.post(
    "/book/{bookUid}", response_model=BookModel, dependencies=[userRoleChecker]
)
async def addTagsToBook(
    bookUid: str, tagData: TagAddModel, session: AsyncSession = Depends(getSession)
) -> BookModel:

    bookWithTag = await tagService.addTagsToBook(
        bookUid=bookUid, tagData=tagData, session=session
    )

    return bookWithTag


@tagsRouter.put("/{tagUid}", response_model=TagModel, dependencies=[userRoleChecker])
async def updateTag(
    tagUid: str,
    tagUpdateData: TagCreateModel,
    session: AsyncSession = Depends(getSession),
) -> TagModel:
    updatedTag = await tagService.updateTag(tagUid, tagUpdateData, session)

    return updatedTag


@tagsRouter.delete(
    "/{tagUid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[userRoleChecker],
)
async def deleteTag(tagUid: str, session: AsyncSession = Depends(getSession)) -> None:
    updatedTag = await tagService.deleteTag(tagUid, session)

    return updatedTag
