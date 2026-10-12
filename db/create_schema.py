from db.models import Base
from db.create_connection import engine

from sqlalchemy import MetaData

metadata = MetaData()
Base.metadata.create_all(engine)