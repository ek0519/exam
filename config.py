import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    MAIL_API_KEY: str
    MAIL_API_SECRET: str
    MAIL_FROM: str
    APP_URL: str

    class Config:
        env_file = os.path.dirname(os.path.abspath(__file__)) + '/.env'
        env_file_encoding = 'utf-8'


settings = Settings()
