from pydantic import BaseSettings


class Settings(BaseSettings):
    rabbitmq_host: str

settings = Settings()