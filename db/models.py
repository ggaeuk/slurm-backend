from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Table

from .database import Base


class JobComp(Base):
    __tablename__ = "jobcomp_table"
    __table__ = Table('jobcomp_table', Base.metadata,
                      Column('jobid', Integer, primary_key=True),
                      Column('uid', Integer, nullable=False),
                      Column('user_name', Text, nullable=False),
                      Column('gid', Integer, nullable=False),
                      Column('group_name', Text, nullable=False),
                      Column('name', Text, nullable=False),
                      Column('state', Integer, nullable=False),
                      Column('partition', Text, nullable=False),
                      Column('timelimit', Text, nullable=False),
                      Column('starttime', Integer, nullable=False, default=0),
                      Column('endtime', Integer, nullable=False, default=0),
                      Column('nodelist', Integer),
                      Column('nodecnt', Text, nullable=False),
                      Column('proc_cnt', Integer, nullable=False),
                      Column('connect_type', Text),
                      Column('reboot', Text),
                      Column('rotate', Text),
                      Column('maxprocs', Integer, nullable=False, default=0),
                      Column('geometry', Text),
                      Column('start', Text),
                      Column('blockid', Integer),
                      )


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)

    topics = relationship("Topic", back_populates="owner")
    posts = relationship("Post", back_populates="owner")


class Topic(Base):
    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)

    owner = relationship("User", back_populates="topics")
    posts = relationship("Post", back_populates="topic")


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    content = Column(Text())
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    topic_id = Column(Integer, ForeignKey("topics.topic_id"))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)

    owner = relationship("User", back_populates="posts")
    topic = relationship("Topic", back_populates="posts")
