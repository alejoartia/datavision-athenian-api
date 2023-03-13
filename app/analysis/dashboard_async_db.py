import databases
import sqlalchemy

metadata = sqlalchemy.MetaData()

DATABASE_URL = "postgresql+psycopg2://postgres:password@db:5432/book_db"

database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
table_file_csv = sqlalchemy.Table("file_csv", metadata, autoload=True, autoload_with=engine)

metadata.create_all(engine)


async def connect():
    await database.connect()


async def disconnect():
    await database.disconnect()
