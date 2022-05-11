import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    APP_URL: str

    class Config:
        env_file = os.path.dirname(os.path.abspath(__file__)) + '/.env'
        env_file_encoding = 'utf-8'


settings = Settings()
