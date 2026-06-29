import os

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "<PASSWORD>"
    DB_NAME: str = "SFMShop"

    jwt_secret: str = "your-jwt-secret"
    JWT_ACCESS_COOKIE_NAME: str = "jwt"
    JWT_TOKEN_LOCATION: list[str] = ["headers"]
    rate_limit_login: str = "5/minute"

    admin_email: str = "<EMAIL>"
    admin_password: str = "<PASSWORD>"
    admin_first_name: str = "admin"
    admin_middle_name: str = "admin"
    admin_last_name: str = "admin"

    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"))


settings = Settings()
