from pydantic import BaseModel, SecretStr


class MySQLConfig(BaseModel):
    host: str
    user: str
    password: SecretStr
    port: int
    database: str


class FlaskConfig(BaseModel):
    port: int
    host: str
    secret_key: SecretStr
    session_type: str
    session_permanent: bool