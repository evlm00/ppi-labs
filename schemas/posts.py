from datetime import datetime

from pydantic import BaseModel, Field


class Post(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class PostPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PostCreate(Post):
    pass


class PostRead(Post):
    id: int
