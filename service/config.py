from pydantic import BaseSettings


class Settings(BaseSettings):
    dbname: str
    sql_alchemy_database_path: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
print(settings)
