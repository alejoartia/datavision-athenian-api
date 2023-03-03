# app/index.py

from fastapi import FastAPI
from sqlalchemy.orm import Session

from .database import Base, engine
from app.routes.app import get_user_stats, save_stats, saved_analysis_list, saved_analysis_object, review_stats, get_data, upload_file

app = FastAPI()

# override database URL for testing
DATABASE_URL = "sqlite:///:memory:"

# create database tables
Base.metadata.create_all(bind=engine)


# dependency to provide a database session for each request
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


# include routes
app.include_router(get_user_stats.router)
app.include_router(save_stats.router)
app.include_router(saved_analysis_list.router)
app.include_router(saved_analysis_object.router)
app.include_router(review_stats.router)
app.include_router(get_data.router)
app.include_router(upload_file.router)



