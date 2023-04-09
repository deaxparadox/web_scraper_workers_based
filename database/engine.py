from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import context

config = context.config()

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:136900@127.0.0.1:5432/scrape"
SQLALCHEMY_DATABASE_URL = config.get_main_option("sqlalchemy.url")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
session_maker = sessionmaker(bind=engine)

