from typing import Union

from pydantic import BaseModel
from datetime import datetime


class JobComp(BaseModel):
    jobid: int
    user_name: str
    name: str
    state: int
    partition: str
    starttime: datetime
    endtime: datetime
    nodelist: str

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: Union[str, None] = None


class PostCreate(PostBase):
    topic_id: int
    owner_id: int


class PostUpdate(PostBase):
    topic_id: int


class Post(PostBase):
    post_id: int
    owner_id: int
    topic_id: int
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True


class TopicBase(BaseModel):
    topic_name: str


class TopicCreate(TopicBase):
    owner_id: int


class TopicUpdate(TopicBase):
    pass


class Topic(TopicBase):
    topic_id: int
    owner_id: int
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int
    topics: list[Topic] = []
    posts: list[Post] = []
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True
