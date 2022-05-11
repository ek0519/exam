from sqlmodel import create_engine, SQLModel
from urllib.parse import quote

from config import settings

host = settings.DB_HOST
db_name = settings.DB_NAME
user = settings.DB_USERNAME
password = quote(settings.DB_PASSWORD)
# engine = create_engine("sqlite:///exam.db", connect_args=connect_args)
engine = create_engine(
  f"postgresql+psycopg2://{user}:{password}@{host}/{db_name}"
)


def create_db_and_tables():
  SQLModel.metadata.create_all(engine)
