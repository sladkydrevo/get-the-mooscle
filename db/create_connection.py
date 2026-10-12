from sqlalchemy import create_engine

from config.settings import settings as cfg


def get_engine(host: str, user: str, password: str, port: int, database: str):
  connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  engine = create_engine(connection_string)
  return engine


engine = get_engine(
  cfg.mysql.host, 
  cfg.mysql.user, 
  cfg.mysql.password.get_secret_value(), 
  cfg.mysql.port,
  cfg.mysql.database
)