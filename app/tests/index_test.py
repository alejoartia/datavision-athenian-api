from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base


from app.routes.app import get_user_stats, save_stats, saved_analysis_list, saved_analysis_object, review_stats, \
    get_data, upload_file, dashboard
from sqlalchemy import create_engine
Base = declarative_base()

# create an engine object for SQLite
engine = create_engine('sqlite:///mydatabase.db')
app = FastAPI()
app.include_router(dashboard)

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
app.include_router(get_user_stats)
app.include_router(save_stats)
app.include_router(saved_analysis_list)
app.include_router(saved_analysis_object)
app.include_router(review_stats)
app.include_router(get_data)
app.include_router(upload_file)



