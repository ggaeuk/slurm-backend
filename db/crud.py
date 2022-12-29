from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def get_job_completion(db: Session, username: str, skip: int = 0, limit: int = 100):
    count = db.query(models.JobComp).filter(models.JobComp.user_name == username).count()
    rowset = db.query(models.JobComp).filter(models.JobComp.user_name == username).order_by(models.JobComp.jobid.desc()).offset(skip).limit(limit).all()
    return {"count": count, "rowset": rowset}


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        created=datetime.now(),
        modified=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_topic(db: Session, topic_id: int):
    topic = db.query(models.Topic).filter(models.Topic.topic_id == topic_id).first()
    return topic


def get_topics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Topic).offset(skip).limit(limit).all()


def create_topic(db: Session, topic: schemas.TopicCreate):
    db_topic = models.Topic(
        **topic.dict(), ## schemas.TopicCreate에서 선언한 column 값들을 다 가져옴. (topic_name, owner_id)
        created=datetime.now(),
        modified=datetime.now()
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def update_topic(db: Session, topic: schemas.TopicUpdate, topic_id: int):
    db_topic = db.query(models.Topic).filter_by(topic_id = topic_id).first()
    db_topic.topic_name = topic.topic_name
    db_topic.modified = datetime.now()
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def delete_topic(db: Session, topic_id: int):
    db_topic = db.query(models.Topic).filter_by(topic_id = topic_id).first()
    db.delete(db_topic)
    db.commit()
    return db_topic


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.post_id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(
        **post.dict(),
        created=datetime.now(),
        modified=datetime.now()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post: schemas.PostUpdate, post_id: int):
    db_post = db.query(models.Post).filter_by(post_id = post_id).first()
    db_post.title = post.title
    db_post.content = post.content
    db_post.topic_id = post.topic_id
    db_post.modified = datetime.now()
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter_by(topic_id = post_id).first()
    db.delete(db_post)
    db.commit()
    return db_post
