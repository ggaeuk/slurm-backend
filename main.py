from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine
from account import types
from account import auth
from slurm import slurmrest
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = file.file.read()
    return {"filename": contents}


@app.get("/slurm/jobcomp/", response_model=dict)
def slurm_jomcomp(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), username: str = Depends(auth.user)):
    return crud.get_job_completion(db, skip=skip, limit=limit, username=username)


# @app.post("/slurm/jwt/")
# def get_jwt_token(username: str = Depends(auth.user)):
#     return slurmrest.get_slurm_jwt(username)


@app.post("/slurm/submit/")
def submit_job(job: dict, username: str = Depends(auth.user)):
    return slurmrest.submit_job(username, job)


@app.get("/slurm/ping/")
def slurm_ping(username: str = Depends(auth.user)):
    return slurmrest.get_slurm_ping(username)


@app.get("/slurm/diag/")
def slurm_ping(username: str = Depends(auth.user)):
    return slurmrest.get_slurm_diag(username)


@app.get("/slurm/nodes/")
def slurm_nodes(username: str = Depends(auth.user)):
    return slurmrest.get_slurm_nodes(username)


@app.get("/slurm/jobs/")
def slurm_jobs(username: str = Depends(auth.user)):
    return slurmrest.get_slurm_jobs(username)


@app.delete("/slurm/job/{job_id}/")
def slurm_delete_job(job_id: int, username: str = Depends(auth.user)):
    return slurmrest.delete_job(username, job_id)


@app.post("/login/", response_model=types.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    token = auth.login(form_data.username, form_data.password)
    ## Keycloak에는 계정이 있지만 DB에는 계정 정보가 없으면 읽어 와서 insert 한다.
    if crud.get_user_by_name(db, username=form_data.username) is None:
        userinfo = auth.userinfo(token)
        user = schemas.UserCreate(username=userinfo['preferred_username'], email=userinfo['email'])
        crud.create_user(db=db, user=user)
    return token


@app.post("/logout/")
def logout(logout: types.Logout):
    return auth.logout(logout=logout)


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_name(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), username: str = Depends(auth.user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), username: str = Depends(auth.user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.patch("/topics/{topic_id}/", response_model=schemas.Topic)
def update_topic(topic_id: int, topic: schemas.TopicUpdate, db: Session = Depends(get_db), username: str = Depends(auth.user)):
    return crud.update_topic(db, topic=topic, topic_id=topic_id)


@app.post("/topics/", response_model=schemas.Topic)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    return crud.create_topic(db=db, topic=topic)


@app.get("/topics/{topic_id}", response_model=schemas.Topic)
def read_topic(topic_id: int, db: Session = Depends(get_db)):
    db_topic = crud.get_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_topic


@app.get("/topics/", response_model=list[schemas.Topic])
def read_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    topics = crud.get_topics(db, skip=skip, limit=limit)
    return topics


@app.delete("/topics/{topic_id}", response_model=schemas.Topic)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    db_topic = crud.delete_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_topic


@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)


@app.patch("/posts/{post_id}/", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    return crud.update_post(db, post=post, post_id=post_id)


@app.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.delete_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
