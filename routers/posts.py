import contextlib

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, status
from database import create_all_tables, get_async_session
from models.posts import Post

from schemas import posts

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


router = APIRouter(lifespan=lifespan)

router.redirect_slashes = False

async def get_post_or_404(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Post:
    select_query = select(Post).where(Post.id == id)
    result = await session.execute(select_query)
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return post


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


@router.get("/", response_model=list[posts.PostRead])
async def list_posts(
    pagination: tuple[int, int] = Depends(pagination),
    session: AsyncSession = Depends(get_async_session),
) -> Sequence[Post]:
    skip, limit = pagination
    select_query = select(Post).offset(skip).limit(limit)
    result = await session.execute(select_query)

    return result.scalars().all()


@router.get("/{id}", response_model=posts.PostRead)
async def get_post(post: Post = Depends(get_post_or_404)) -> Post:
    return post


@router.post(
    "/", response_model=posts.PostRead, status_code=status.HTTP_201_CREATED
)
async def create_post(
    post_create: posts.PostCreate, session: AsyncSession = Depends(get_async_session)
) -> Post:
    post = Post(**post_create.dict())
    session.add(post)
    await session.commit()

    return post


@router.patch("/{id}", response_model=posts.PostRead)
async def update_post(
    post_update: posts.PostPartialUpdate,
    post: Post = Depends(get_post_or_404),
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    post_update_dict = post_update.dict(exclude_unset=True)
    for key, value in post_update_dict.items():
        setattr(post, key, value)

    session.add(post)
    await session.commit()

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: Post = Depends(get_post_or_404),
    session: AsyncSession = Depends(get_async_session),
):
    await session.delete(post)
    await session.commit()
