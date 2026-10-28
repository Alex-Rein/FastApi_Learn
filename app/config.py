from pydantic import model_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = Field()
    DB_PORT: int = Field()
    DB_USER: str = Field()
    DB_PASS: str = Field()
    DB_NAME: str = Field()

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()

