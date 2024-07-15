from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class RunConfig(BaseModel):
	host: str = '0.0.0.0'
	port: int = 8001


class ApiPrefix(BaseModel):
	prefix: str = '/api'


class DatabaseConfig(BaseModel):
	url: PostgresDsn
	echo: bool = False,
	echo_pool: bool = False,
	pool_size: int = 50,
	max_overflow: int = 10


class Settings(BaseSettings):
	run: RunConfig = RunConfig()
	api: ApiPrefix = ApiPrefix()
	db: DatabaseConfig


settings = Settings()
